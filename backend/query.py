from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

@app.post("/query")
def query_knowledge_base(request: QueryRequest):
    try:
        results = db.similarity_search(
            request.question,
            k=4,
            filter={
                "$and": [
                    {"region": "Manipur"},
                    {"domain": "Agriculture"}
                ]
            }
        )

        if not results:
            return {"answer": "No relevant documents found."}

        context = "\n\n".join([doc.page_content for doc in results])

        return {
            "answer": context[:1500],
            "sources": [doc.metadata for doc in results]
        }

    except Exception as e:
        return {"error": str(e)}

