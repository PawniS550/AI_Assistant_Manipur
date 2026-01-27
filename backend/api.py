from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

import os

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI()

# ----------------------------
# CORS (important for frontend fetch)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Request schema
# ----------------------------
class QueryRequest(BaseModel):
    question: str
    region: str | None = None
    domain: str | None = None

# ----------------------------
# Embeddings
# ----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ----------------------------
# Chroma DB
# ----------------------------
PERSIST_DIR = "chroma_db"

if not os.path.exists(PERSIST_DIR):
    raise RuntimeError(
        "Chroma DB not found. Run ingest.py first to create embeddings."
    )

db = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings
)

# ----------------------------
# Query endpoint
# ----------------------------
@app.post("/query")
def query_knowledge_base(req: QueryRequest):

    # ---- Build Chroma filter correctly ----
    where_filter = None

    if req.region and req.domain:
        where_filter = {
            "$and": [
                {"region": req.region},
                {"domain": req.domain}
            ]
        }
    elif req.region:
        where_filter = {"region": req.region}
    elif req.domain:
        where_filter = {"domain": req.domain}

    # ---- Similarity search ----
    docs = db.similarity_search(
        req.question,
        k=5,
        filter=where_filter
    )

    if not docs:
        return {
            "question": req.question,
            "answer": "No relevant information found.",
            "sources": []
        }

    # ---- Prepare response ----
    answer = "\n\n".join([doc.page_content for doc in docs])

    sources = list(
        set(
            doc.metadata.get("source", "unknown")
            for doc in docs
        )
    )

    return {
        "question": req.question,
        "answer": answer,
        "sources": sources
    }

# ----------------------------
# Health check
# ----------------------------
@app.get("/")
def health():
    return {"status": "API running"}

