# RateMyProfessor Review Collection

This directory stores one normalized markdown file per SFSU CS professor.

## Workflow

1. Verify each professor's SFSU RateMyProfessor page.
2. Record the result in `documents/raw/rmp_professors.txt` as `Name | URL`.
3. Omit professors with no verified professor page.
4. Open the verified RMP page.
5. Browse normally, letting the page load and scrolling/loading reviews only when needed.
6. Paste `scripts/rmp_console_scraper.js` into DevTools Console once.
7. Save the copied markdown output to this directory using `lastname_firstname.md`.
8. Validate each batch of 5 files with `./.venv/bin/python scripts/validate_rmp_batch.py`.

Stop immediately if RateMyProfessor shows a CAPTCHA, access denial, abnormal loading, repeated empty extraction, or obvious rate limiting. Resume later instead of trying to bypass it.

Professors with verified RMP pages but zero ratings are tracked in `documents/raw/rmp_zero_ratings.txt` and do not get empty markdown files.

## Filename Targets

- `souza_anthony.md`
- `ta_duc.md`
- `hsu_william.md`
- `tomasevich_daniel.md`
- `wang_jingyi.md`
- `kroll_lawrence.md`
- `moore_kimbrough.md`
- `scott_andrew.md`
- `hui_hugh.md`
- `mehta_karun.md`
- `yang_hui.md`
- `ortiz_jose_costa.md`
- `bierman_robert.md`
- `sun_timothy.md`
- `okada_kazunori.md`
- `pico_matt.md`
- `chen_xuhui.md`
- `kulkarni_anagha.md`
- `hui_joseph.md`
- `humayoun_shahrukh.md`
- `wang_qun.md`
- `bethel_e_wes.md`
- `petkovic_dragutin.md`
- `song_isabel_hyo_jung.md`
- `sikder_abdur.md`
- `de_silva_akila.md`
- `el_alaoui_sara.md`

## Spot Checks

- Header includes `COURSE: Multiple`, `SOURCE: RateMyProfessor`, `PROFESSOR`, `SCHOOL`, and `OVERALL`.
- File contains 1 to 30 reviews.
- Course labels and tags are preserved where present.
- No review block has empty review text.
- Professor name in the header matches the expected professor for the filename.
