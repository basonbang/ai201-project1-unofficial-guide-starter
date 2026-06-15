# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My domain is an unofficial guide for CS courses at SFSU. While the official course catalog tells you what a course covers, the information students actually need — how difficult the exams are, which professors are worth taking, how much time a course demands per week, which sections to avoid — is scattered across Discord servers, Reddit threads, Rate My Professor reviews, and past syllabi that most incoming students don't know to look for. This RAG system mimics the experience of asking an upperclassman: it surfaces institutional memory that lives only in student communities and isn't indexed anywhere a freshman would naturally search.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Syllabus | CSC 648 (Software Engineering) — Souza; grading, milestones, team structure | `documents/syllabi/csc648_syllabus_anthonysouza.txt` |
| 2 | Syllabus | CSC 415 (Operating Systems) — Bierman; grading breakdown, project list | `documents/syllabi/csc415_syllabus_robertbierman.txt` |
| 3 | Syllabus | CSC 413 (Software Development) — Souza; assignments, exam weight | `documents/syllabi/csc413_syllabus_anthonysouza.txt` |
| 4 | Syllabus | CSC 340 (Programming Methodology) — Duc Ta; two sections for comparison | `documents/syllabi/csc340_syllabus_ducta.pdf` |
| 5 | Syllabus | CSC 317 (Web Development) — Souza; project structure, grading | `documents/syllabi/csc317_syllabus_anthonysouza.pdf` |
| 6 | Syllabus | CSC 510 (Software Engineering Process) — Ortiz | `documents/syllabi/csc510_syllabus_joseortiz.pdf` |
| 7 | Discord | CSC 648 channel — professor comparisons, team tips, workload, 2021–2023 | `documents/discord/csc648_discord.md` |
| 8 | Discord | CSC 600 channel — multi-year thread archive (2021–2025); large volume | `documents/discord/csc600_discord_2024.md` |
| 9 | Discord | CSC 415 channel — OS project difficulty, exam tips | `documents/discord/csc415_discord.md` |
| 10 | Discord | CSC 413 channel — workload, professor style, project advice | `documents/discord/csc413_discord.md` |
| 11 | Discord | class-reviews channel (2021–2025) — cross-course general reviews and warnings | `documents/discord/class-reviews_discord_2024.md` |
| 12 | Discord | CSC 675 channel — DB course tips, professor Hui | `documents/discord/csc675_discord.md` |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** ~400 tokens (~1,600 characters)

**Overlap:** ~50 tokens for syllabi sections; 0 for Discord thread blocks

**Reasoning:** Documents have two distinct structures that warrant different splitting logic, but the same size target:

- **Discord files** are pre-segmented into thread blocks delimited by `---`. Each block is one reply chain — a semantically atomic unit (question + responses). Splitting at `---` boundaries produces chunks that are already the right size (50–300 words) and should not be broken mid-thread. Overlap is unnecessary because threads don't share context across boundaries.
- **Syllabi** are structured Markdown/text with section headings. Splitting on `##` headings keeps each chunk topically coherent (e.g., "Grading" stays with its breakdown). Sections can run long, so a 400-token cap with ~50-token overlap prevents a long section from producing one giant chunk while preserving sentence context at split points.

400 tokens is large enough to hold a complete thread exchange or a full grading breakdown, but small enough that `all-MiniLM-L6-v2`'s 256-token sequence limit still captures the most important content near the start of each chunk. Chunks that exceed 256 tokens will be truncated by the embedding model, so keeping the most signal-dense content (the question and direct answer) near the top of each chunk is important.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers` (local, no API cost)

**Top-k:** 5

**Production tradeoff reflection:** `all-MiniLM-L6-v2` is a strong default — fast, free, and good at semantic similarity on short conversational text. Its main limitation is the 256-token sequence cap: any chunk longer than that gets silently truncated before embedding, which is why chunking is kept tight. In a production deployment with no cost constraint, the main tradeoffs to weigh would be:

- **Context length**: `all-mpnet-base-v2` or `text-embedding-3-large` (OpenAI) support much longer sequences — important if syllabi sections run long and truncation loses grading details.
- **Domain specificity**: A model fine-tuned on student Q&A or educational text (e.g., from a university forum corpus) would likely outperform a general-purpose model on retrieval precision for course-specific jargon ("curve," "10% attendance," "5 sprints"). No such model is readily available off-the-shelf.
- **Multilingual support**: Not needed here — all documents are English.
- **Latency**: `all-MiniLM-L6-v2` runs in ~5ms per chunk on CPU. `text-embedding-3-large` via API adds network round-trips and ~$0.13/million tokens. For a low-traffic internal tool the cost is negligible, but local inference stays preferable for a student project with no API budget.

Metadata fields (`COURSE`, `SOURCE`, `DATE`) are stored in ChromaDB but not filtered by default. A `where` clause (e.g., `{"COURSE": "CSC 648"}`) will be added if evaluation shows cross-course retrieval contaminating answers.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about the workload in CSC 648? | Heavy workload; project-heavy with 5 sprints; team coordination is the main challenge |
| 2 | Is CSC 415 hard and what should I know going in? | Regarded as one of the harder upper-division courses; requires solid C skills; OS concepts (processes, memory management, file systems) are tested heavily |
| 3 | What professor teaches CSC 675 and is the course recommended? | Joseph Hui; generally regarded as a solid database course; workload is moderate and lectures are well-organized |
| 4 | What are the grading components for CSC 648 according to the syllabus? | Based on syllabus: team project milestones, sprint demos, individual contributions tracked via GitHub; no traditional exams |
| 5 | How has student opinion of CSC 600 changed over the years? | Consistent reputation as one of the harder grad courses; workload and difficulty complaints appear across 2021–2024 threads |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Chunk boundary splitting in Discord threads**: Discord messages are short and conversational — a question and its accepted answer often span 3–5 separate messages posted minutes apart. A fixed-character chunker will frequently cut mid-conversation, leaving a chunk that contains a question with no answer, or an answer with no question. Retrieval then returns incomplete context and the LLM can't give a useful response. Mitigation: split on `---` block separators (which already mark thread boundaries in the exported .md files) rather than on raw character count.

2. **Professor name and course nickname OOV collisions**: Students refer to courses by number only ("648"), by nickname ("softeng"), or by professor last name ("Souza's class"). The `all-MiniLM-L6-v2` model has no course-specific vocabulary — "Souza" and "Bierman" are treated as opaque tokens with no semantic neighborhood. A query like "is Souza's 648 worth it?" may retrieve chunks about a different Souza course or miss the right ones entirely. Mitigation: store course number and professor name as ChromaDB metadata fields so keyword-level disambiguation can be layered on top of semantic similarity if evaluation reveals the problem.

---

## Architecture

```
documents/discord/*.md          documents/syllabi/*.txt
         │                               │
         └──────────────┬────────────────┘
                        ▼
            ┌─────────────────────┐
            │  Stage 1: Ingestion │  open() — read .md and .txt files
            │  load_documents()   │  output: [{text, source}, ...]
            └──────────┬──────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │  Stage 2: Chunking  │  split on "---" (Discord) or "##" (syllabi)
            │  chunk_documents()  │  chunk_size=400 tokens, overlap=50
            └──────────┬──────────┘  output: [{text, source, chunk_id}, ...]
                       │
                       ▼
            ┌──────────────────────────┐
            │  Stage 3: Embed + Store  │  sentence-transformers: all-MiniLM-L6-v2
            │  build_vector_store()    │  chromadb: persistent .chroma/ collection
            └──────────┬───────────────┘
                       │
              query at runtime
                       │
                       ▼
            ┌─────────────────────┐
            │  Stage 4: Retrieval │  embed query → ChromaDB .query() → top-5 chunks
            │  retrieve()         │
            └──────────┬──────────┘
                       │
                       ▼
            ┌─────────────────────┐
            │  Stage 5: Generation│  groq: llama-3.1-8b-instant
            │  generate()         │  grounded system prompt + source attribution
            └─────────────────────┘
                       │
                       ▼
              CLI output to user
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
- Tool: Claude Code
- Input: the Documents table and Chunking Strategy section of this planning.md, plus the file structure of `documents/`
- Expected output: `load_documents()` function that walks `documents/discord/` and `documents/syllabi/` and returns `[{text, source}]`; `chunk_documents()` that splits on `---` for Discord files and `##` headings for syllabi, with a 400-token fallback cap
- Verification: print the first 5 chunks and their source names; confirm no chunk is over 500 characters; confirm source attribution is correct

**Milestone 4 — Embedding and retrieval:**
- Tool: Claude Code
- Input: Retrieval Approach section of this planning.md, plus the chunk output format from Milestone 3
- Expected output: `build_vector_store()` that embeds all chunks with `all-MiniLM-L6-v2` and stores them in a persistent ChromaDB collection; `retrieve()` that embeds a query and returns top-5 chunks with source metadata
- Verification: run 3 of the 5 evaluation questions through `retrieve()` only (no LLM), inspect returned chunks manually to confirm they contain relevant content

**Milestone 5 — Generation and interface:**
- Tool: Claude Code
- Input: grounded system prompt from this planning.md, Groq API docs, the retrieve() output format
- Expected output: `generate()` that builds a context block from retrieved chunks labeled by source, sends to `llama-3.1-8b-instant`, and returns the response; a `while True` CLI loop as the query interface
- Verification: run all 5 evaluation questions end-to-end; check that responses cite source filenames; ask one out-of-scope question and confirm the system refuses rather than hallucinating
