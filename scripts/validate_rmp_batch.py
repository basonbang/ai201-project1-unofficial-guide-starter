#!/usr/bin/env python3
"""Validate manually collected RateMyProfessor markdown files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "documents" / "raw" / "rmp_professors.txt"
ZERO_RATINGS = ROOT / "documents" / "raw" / "rmp_zero_ratings.txt"
RMP_DIR = ROOT / "documents" / "rmp"

HEADER_RE = re.compile(
    r"^## \[COURSE: Multiple\] \[SOURCE: RateMyProfessor\] "
    r"\[PROFESSOR: (?P<professor>[^\]]+)\] "
    r"\[SCHOOL: (?P<school>[^\]]+)\] "
    r"\[OVERALL: (?P<overall>[^\]]+)\]",
    re.MULTILINE,
)
REVIEW_RE = re.compile(
    r"\*\*Review\*\* \[[^\]]+\] - Course: .+? \| Quality: .+?/5 "
    r"\| Grade: .+? \| Would Take Again: .+",
)


FILENAME_OVERRIDES = {
    "E. Wes Bethel": "bethel_e_wes.md",
    "Jose Costa Ortiz": "ortiz_jose_costa.md",
    "Akila De Silva": "de_silva_akila.md",
    "Sara El Alaoui": "el_alaoui_sara.md",
    "Isabel Hyo Jung Song": "song_isabel_hyo_jung.md",
}

NAME_TOKEN_OVERRIDES = {
    "Isabel Hyo Jung Song": ["isabel", "song"],
    "Akila De Silva": ["de", "silva"],
    "Hugh Hui": ["hui", "hugh"],
    "Jose Costa Ortiz": ["ortiz", "costa"],
}


def expected_filename(name: str) -> str:
    if name in FILENAME_OVERRIDES:
        return FILENAME_OVERRIDES[name]

    parts = re.sub(r"[^A-Za-z0-9 ]+", "", name).lower().split()
    if len(parts) < 2:
        return "_".join(parts) + ".md"

    return f"{parts[-1]}_{'_'.join(parts[:-1])}.md"


def load_roster() -> list[tuple[str, str, Path]]:
    entries = []
    for line in ROSTER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" not in line:
            continue
        name, url = [part.strip() for part in line.split("|", 1)]
        entries.append((name, url, RMP_DIR / expected_filename(name)))
    return entries


def load_zero_rating_names() -> set[str]:
    if not ZERO_RATINGS.exists():
        return set()

    names = set()
    for line in ZERO_RATINGS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        name, _ = [part.strip() for part in line.split("|", 1)]
        names.add(name)
    return names


def validate_file(path: Path, expected_name: str) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    header = HEADER_RE.search(text)

    if not header:
        errors.append("missing or malformed normalized header")
    else:
        professor = header.group("professor").lower()
        expected_tokens = NAME_TOKEN_OVERRIDES.get(
            expected_name,
            re.sub(r"[^a-z0-9 ]+", "", expected_name.lower()).split()[-2:],
        )
        if not all(token in professor for token in expected_tokens):
            errors.append(f"header professor does not match expected name: {expected_name}")

    review_count = len(REVIEW_RE.findall(text))
    if review_count < 1 or review_count > 30:
        errors.append(f"review count must be 1..30, found {review_count}")

    review_blocks = [block.strip() for block in text.split("---") if "**Review**" in block]
    for index, block in enumerate(review_blocks, start=1):
        quote_lines = [line for line in block.splitlines() if line.startswith("> ")]
        quote_text = " ".join(line[2:].strip() for line in quote_lines)
        if not quote_text:
            errors.append(f"review {index} has empty review text")

    if "Quality:" not in text or "Grade:" not in text or "Would Take Again:" not in text:
        errors.append("missing review metadata fields")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files",
        nargs="*",
        help="Optional specific RMP markdown files to validate. Defaults to all expected files that exist.",
    )
    parser.add_argument(
        "--require-all",
        action="store_true",
        help="Fail if any expected RMP markdown file is missing.",
    )
    args = parser.parse_args()

    roster = load_roster()
    zero_rating_names = load_zero_rating_names()
    expected_by_path = {path.resolve(): name for name, _, path in roster}

    if args.files:
        targets = [Path(file).resolve() for file in args.files]
    else:
        targets = [path.resolve() for _, _, path in roster if path.exists()]

    errors = []
    missing = []
    for name, _, path in roster:
        if name in zero_rating_names:
            continue
        if not path.exists():
            missing.append(path)
            continue
        if not args.files or path.resolve() in targets:
            for error in validate_file(path, name):
                errors.append(f"{path.relative_to(ROOT)}: {error}")

    unexpected = sorted(path for path in targets if path not in expected_by_path)
    for path in unexpected:
        errors.append(f"{path.relative_to(ROOT)}: not an expected RMP filename")

    for path in targets:
        if not path.exists():
            errors.append(f"{path.relative_to(ROOT)}: file does not exist")

    if args.require_all:
        for path in missing:
            errors.append(f"{path.relative_to(ROOT)}: expected file is missing")

    if errors:
        print("RMP validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"RMP validation passed for {len(targets)} file(s).")
    if missing and not args.require_all:
        print(f"Pending files: {len(missing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
