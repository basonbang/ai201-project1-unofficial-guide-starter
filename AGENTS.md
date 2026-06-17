# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

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

- `planning.md` — spec document: domain, sources, chunking strategy, retrieval config, evaluation plan, architecture diagram. Fill this out before writing pipeline code.
- `README.md` — submission document: fill out every section after building and testing each pipeline stage.
- `documents/` — place raw source documents here (text, markdown, or PDF files).
- `requirements.txt` — core deps listed; optional deps (UI, PDF) are commented out.
