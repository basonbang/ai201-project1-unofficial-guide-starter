# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CodePath AI201 Project 1: a RAG (Retrieval Augmented Generation) system called "The Unofficial Guide." The system answers questions using a domain-specific document corpus, grounding responses only in retrieved content.

Five-stage pipeline:
1. **Document Ingestion** — load raw documents from `documents/`
2. **Chunking** — split documents into chunks with configurable size and overlap
3. **Embedding + Vector Store** — embed chunks with `sentence-transformers`, store in ChromaDB
4. **Retrieval** — embed query, retrieve top-k chunks from ChromaDB
5. **Generation** — pass retrieved chunks to Groq LLM with a grounding system prompt

## Setup

```bash
# Activate the virtualenv (Python 3.13, already created)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and fill in your API key
cp .env.example .env
# Then set GROQ_API_KEY in .env
```

## Environment

- **GROQ_API_KEY** — required, free key from console.groq.com. Loaded via `python-dotenv`.
- **`.venv/`** — pre-created virtualenv, use it directly rather than creating a new one.

## Key Libraries

| Library | Role |
|---|---|
| `sentence-transformers` | Local embedding model (e.g. `all-MiniLM-L6-v2`) |
| `chromadb` | Local vector store for chunk embeddings |
| `groq` | LLM API for grounded response generation |
| `python-dotenv` | Load `.env` into environment |
| `gradio` or `streamlit` | Query interface (optional, uncomment in requirements.txt) |
| `pdfplumber` | PDF ingestion (optional, uncomment if documents/ has PDFs) |

## Project Files

- `planning.md` — spec document: domain, sources, chunking strategy, retrieval config, evaluation plan, architecture diagram. Actively updated as the project progresses.
- `README.md` — submission document: fill out every section after building and testing each pipeline stage. Actively updated.
- `documents/` — full corpus, organized by source type (see below).
- `pipeline.py` — main pipeline script. Currently contains boilerplate stubs for all 5 stages; nothing is wired up yet.
- `requirements.txt` — core deps listed; optional deps (UI, PDF) are commented out.
- `scripts/` — one-off ingestion utilities used during document acquisition (not part of the pipeline).

## Current Project State

**Phase: Document ingestion complete. Pipeline implementation starting.**

All source documents have been gathered and normalized. The corpus is fully assembled in `documents/` and ready for the pipeline to ingest.

### Corpus Overview

| Folder | Contents |
|---|---|
| `documents/syllabi/` | 15 PDF/DOCX/TXT syllabi for core CS courses |
| `documents/discord/` | 40 normalized markdown files from 28 Discord channels (2021–2025), preprocessed into thread-preserved blocks |
| `documents/rmp/` | 28 markdown files, one per active Fall 2026 professor (up to 30 most recent reviews each) |
| `documents/catalog/` | 47 markdown files from the SFSU course catalog, one per CS course offered this fall |
| `documents/raw/` | Raw source files (Discord JSON exports, professor URL list) — not ingested by the pipeline |

### Normalized Document Format

Every document in `documents/` (except `raw/`) follows this header schema:
```
## [COURSE: CSC XXX] [SOURCE: Discord|RMP|Syllabus|Catalog] [DATE: ...]
```
These header fields are extracted as ChromaDB metadata at ingestion time.

### Pipeline Status

`pipeline.py` has the correct constants and imports, and stub functions for all 5 stages, but none are implemented yet:
- `CHUNK_SIZE = 1600` characters, `CHUNK_OVERLAP = 200`
- `EMBEDDING_MODEL = "all-MiniLM-L6-v2"`
- `TOP_K = 5`
- `GROQ_MODEL = "llama-3.1-8b-instant"`

### Scripts (ingestion-only, not part of pipeline)

- `scripts/rmp_console_scraper.js` — browser DevTools script used to scrape RMP reviews
- `scripts/validate_rmp_batch.py` — validation script for checking RMP markdown output
