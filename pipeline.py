import os
import glob
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = ".chroma"
COLLECTION_NAME = "unofficial_guide"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 1600   # characters (~400 tokens)
CHUNK_OVERLAP = 200  # characters (~50 tokens)
TOP_K = 5
GROQ_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """You are the Unofficial Guide for SFSU CS courses. \
Answer the student's question using ONLY the information in the retrieved \
excerpts provided below. Each excerpt is labeled with its source file. \
Cite the source filename in your answer (e.g. "According to csc648_discord.md, ..."). \
If the excerpts do not contain enough information to answer the question, respond \
with exactly: "I don't have enough information in my documents to answer that." \
Do not use any outside knowledge."""


# ---------------------------------------------------------------------------
# Stage 1: Ingestion
# ---------------------------------------------------------------------------

def load_documents(docs_root: str = "documents") -> list[dict]:
    documents = []
    for pattern in ["discord/*.md", "syllabi/*.txt"]:
        for path in sorted(glob.glob(os.path.join(docs_root, pattern))):
            with open(path, encoding="utf-8", errors="ignore") as f:
                text = f.read()
            documents.append({"text": text, "source": Path(path).name})
    print(f"[Ingestion] Loaded {len(documents)} documents")
    return documents


# ---------------------------------------------------------------------------
# Stage 2: Chunking
# ---------------------------------------------------------------------------

def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return [c for c in chunks if c]


def chunk_documents(documents: list[dict]) -> list[dict]:
    chunks = []
    for doc in documents:
        text = doc["text"]
        source = doc["source"]

        if source.endswith(".md"):
            # Split Discord exports on thread-separator lines
            blocks = [b.strip() for b in text.split("\n---\n") if b.strip()]
        else:
            # Split syllabi on section headings
            import re
            blocks = [b.strip() for b in re.split(r"\n(?=##)", text) if b.strip()]

        for block in blocks:
            if len(block) <= CHUNK_SIZE:
                chunks.append({"text": block, "source": source})
            else:
                # Block is too large — apply sliding window
                for sub in _chunk_text(block, CHUNK_SIZE, CHUNK_OVERLAP):
                    chunks.append({"text": sub, "source": source})

    for i, chunk in enumerate(chunks):
        chunk["chunk_id"] = f"{chunk['source']}_{i}"

    print(f"[Chunking] Produced {len(chunks)} chunks")
    return chunks


# ---------------------------------------------------------------------------
# Stage 3: Embedding + Vector Store
# ---------------------------------------------------------------------------

def build_vector_store(chunks: list[dict]) -> chromadb.Collection:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    if collection.count() > 0:
        print(f"[Vector Store] Collection already has {collection.count()} chunks — skipping re-embed")
        return collection

    model = SentenceTransformer(EMBEDDING_MODEL)
    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]

    print(f"[Embedding] Encoding {len(texts)} chunks with {EMBEDDING_MODEL}…")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64).tolist()

    # ChromaDB has a 41665-item add limit; batch if needed
    batch_size = 5000
    for i in range(0, len(texts), batch_size):
        collection.add(
            documents=texts[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            ids=ids[i:i+batch_size],
        )

    print(f"[Vector Store] Stored {collection.count()} chunks in {CHROMA_PATH}/")
    return collection


# ---------------------------------------------------------------------------
# Stage 4: Retrieval
# ---------------------------------------------------------------------------

_embed_model = None

def _get_embed_model() -> SentenceTransformer:
    global _embed_model
    if _embed_model is None:
        _embed_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embed_model


def retrieve(query: str, collection: chromadb.Collection) -> list[dict]:
    model = _get_embed_model()
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=TOP_K)
    hits = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        hits.append({"text": text, "source": meta["source"]})
    return hits


# ---------------------------------------------------------------------------
# Stage 5: Generation
# ---------------------------------------------------------------------------

def generate(query: str, hits: list[dict]) -> str:
    context_parts = []
    for i, hit in enumerate(hits, 1):
        context_parts.append(f"[{i}] Source: {hit['source']}\n{hit['text']}")
    context = "\n\n".join(context_parts)

    user_message = f"Retrieved excerpts:\n\n{context}\n\nQuestion: {query}"

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    collection = build_vector_store(chunks)

    print("\nUnofficial Guide ready. Type 'quit' to exit.\n")
    while True:
        query = input("Ask a question: ").strip()
        if not query:
            continue
        if query.lower() in {"quit", "exit", "q"}:
            break
        hits = retrieve(query, collection)
        answer = generate(query, hits)
        print(f"\n{answer}\n")
