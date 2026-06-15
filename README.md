# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This system covers student-generated knowledge about CS courses at SFSU: professor teaching styles, exam difficulty, workload, which electives to take and in what order, and general course-taking strategy. This knowledge is valuable because it reflects real student experience rather than administrative descriptions — but it's hard to find through official channels because it lives in ephemeral spaces: Discord servers you have to be invited to, Reddit threads that get buried, Rate My Professor entries without course context, and syllabi that aren't publicly archived. A new student or prospective transfer has no single place to look. This system mimics the experience of asking an upperclassman for advice: it retrieves the right fragment of collective memory for whatever question you're trying to answer.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | CSC 648 syllabus — Souza | Syllabus (TXT) | `documents/syllabi/csc648_syllabus_anthonysouza.txt` |
| 2 | CSC 415 syllabus — Bierman | Syllabus (TXT) | `documents/syllabi/csc415_syllabus_robertbierman.txt` |
| 3 | CSC 413 syllabus — Souza | Syllabus (TXT) | `documents/syllabi/csc413_syllabus_anthonysouza.txt` |
| 4 | CSC 340 syllabus — Duc Ta | Syllabus (PDF) | `documents/syllabi/csc340_syllabus_ducta.pdf` |
| 5 | CSC 317 syllabus — Souza | Syllabus (PDF) | `documents/syllabi/csc317_syllabus_anthonysouza.pdf` |
| 6 | CSC 510 syllabus — Ortiz | Syllabus (PDF) | `documents/syllabi/csc510_syllabus_joseortiz.pdf` |
| 7 | CSC 648 Discord channel export | Discord export (MD) | `documents/discord/csc648_discord.md` |
| 8 | CSC 600 Discord channel export (2024) | Discord export (MD) | `documents/discord/csc600_discord_2024.md` |
| 9 | CSC 415 Discord channel export | Discord export (MD) | `documents/discord/csc415_discord.md` |
| 10 | CSC 413 Discord channel export | Discord export (MD) | `documents/discord/csc413_discord.md` |
| 11 | class-reviews Discord channel (2024) | Discord export (MD) | `documents/discord/class-reviews_discord_2024.md` |
| 12 | CSC 675 Discord channel export | Discord export (MD) | `documents/discord/csc675_discord.md` |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** ~400 tokens (~1,600 characters)

**Overlap:** ~50 tokens (~200 characters) for syllabi sections; 0 for Discord thread blocks

**Why these choices fit your documents:** The corpus has two distinct structures that warrant different splitting logic. Discord exports are pre-segmented into thread blocks delimited by `\n---\n` — each block is one reply chain (question + responses), a semantically atomic unit. Splitting at those delimiters produces naturally-sized chunks (50–300 words) that shouldn't be broken mid-thread; overlap adds no value across unrelated conversations. Syllabi are structured text with `##` section headings, so splitting on headings keeps each chunk topically coherent (e.g., the Grading section stays intact). For sections that run long, a 1,600-character sliding window with 200-character overlap prevents oversized chunks while preserving sentence context at split points. The 400-token target also respects `all-MiniLM-L6-v2`'s 256-token sequence limit — chunks that exceed it get silently truncated by the embedding model, so keeping the most signal-dense content near the top of each chunk is important.

**Final chunk count:** TBD — run `python pipeline.py` to populate

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` (local inference, no API cost)

**Production tradeoff reflection:** `all-MiniLM-L6-v2` is a strong default for this use case — fast (~5ms per chunk on CPU), free, and effective at semantic similarity on short conversational text. Its main limitation is the 256-token sequence cap: chunks longer than that get silently truncated before embedding, which is why chunking is kept tight. In a production deployment with no cost constraint, the key tradeoffs to weigh would be:

- **Context length**: `all-mpnet-base-v2` or OpenAI's `text-embedding-3-large` support much longer sequences — important if syllabi sections run long and truncation loses critical grading details.
- **Domain specificity**: A model fine-tuned on student Q&A or educational forum text would likely outperform a general-purpose model on retrieval precision for course-specific jargon ("curve," "10% attendance," "5 sprints"). No such model is readily available off-the-shelf for this domain.
- **Multilingual support**: Not a concern here — all documents are English — but would matter for a university with a multilingual student body.
- **Latency vs. accuracy**: Local inference keeps latency near zero but sacrifices the accuracy gains of larger API-hosted models. For a low-traffic internal tool the cost of `text-embedding-3-large` is negligible, but local inference is preferable for a student project with no API budget.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

```
You are the Unofficial Guide for SFSU CS courses. Answer the student's question
using ONLY the information in the retrieved excerpts provided below. Each excerpt
is labeled with its source file. Cite the source filename in your answer
(e.g. "According to csc648_discord.md, ..."). If the excerpts do not contain
enough information to answer the question, respond with exactly:
"I don't have enough information in my documents to answer that."
Do not use any outside knowledge.
```

The instruction enforces grounding through two mechanisms: (1) the explicit "ONLY the information in the retrieved excerpts" constraint prohibits the model from drawing on parametric knowledge, and (2) the fallback phrase is specified verbatim so the model can't soften a refusal into a hedged answer that still leaks outside information.

**How source attribution is surfaced in the response:** Each retrieved chunk is prepended with a labeled header (`[1] Source: csc648_discord.md`) before being passed to the model. The system prompt instructs the model to cite filenames inline (e.g., "According to csc648_discord.md, ..."), so attribution is visible directly in the response text rather than as a separate footnote.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing the Architecture section of planning.md before touching any code forced a decision about function signatures and data shapes upfront — specifically, that every stage would pass `{"text": ..., "source": ...}` dicts through the pipeline. That shared format made it straightforward to wire `load_documents()` → `chunk_documents()` → `build_vector_store()` without having to refactor interfaces mid-implementation. Without the diagram, it would have been easy to design each stage in isolation and end up with mismatched outputs.

**One way your implementation diverged from the spec, and why:** The spec described chunk size in tokens (400 tokens), but the implementation uses characters (1,600 characters, ~400 tokens at 4 chars/token average). This was a pragmatic choice: Python's `len()` operates on characters, not tokens, and adding a tokenizer just to count tokens before splitting would add a dependency and latency with no meaningful accuracy gain at this scale. The character-based approximation is close enough that the actual chunk sizes still fall within the embedding model's limits.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* The project rubric, the file structure of `documents/` (40 Discord .md exports, 15 syllabi), and a description of the two document types (thread-based Discord exports vs. section-based syllabi text files). I asked Claude Code to fill out the Chunking Strategy and Retrieval Approach sections of planning.md.
- *What it produced:* A chunking strategy using a fixed 400-character sliding window with 50-character overlap, applied uniformly to all documents.
- *What I changed or overrode:* I directed Claude to revise the strategy to split Discord files on `---` thread separators (semantic boundaries) rather than a fixed character window, because Discord messages are already naturally chunked by conversation threads. Applying a sliding window would cut mid-thread and destroy the question-answer structure. The syllabi still use section-heading splits with a character-cap fallback.

**Instance 2**

- *What I gave the AI:* The completed planning.md (all sections: domain, document list, chunking strategy, retrieval approach, architecture diagram, AI tool plan) and the requirements.txt. I asked Claude Code to implement the full pipeline in a single `pipeline.py` file following the five-stage architecture in the spec.
- *What it produced:* A working `pipeline.py` with all five stages (`load_documents`, `chunk_documents`, `build_vector_store`, `retrieve`, `generate`) and a CLI query loop.
- *What I changed or overrode:* The initial version added ChromaDB batch logic with a hardcoded limit of 41,665 items but used a batch size of 5,000 — I reviewed the batching code and confirmed it was correct for large corpora. I also verified the system prompt enforced a verbatim refusal phrase ("I don't have enough information in my documents to answer that.") rather than a softer instruction, to prevent the model from producing hedged answers that still use outside knowledge.
