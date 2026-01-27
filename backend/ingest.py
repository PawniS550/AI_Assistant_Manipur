import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "data"
CHROMA_PATH = "chroma_db"

if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Data folder not found: {DATA_DIR}")

pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]

if not pdf_files:
    raise FileNotFoundError("No PDF files found in data folder")

documents = []

for pdf in pdf_files:
    path = os.path.join(DATA_DIR, pdf)
    loader = PyPDFLoader(path)
    docs = loader.load()
    for d in docs:
        d.metadata["source"] = pdf
        d.metadata["region"] = "Manipur"
        d.metadata["domain"] = "Agriculture"
    documents.extend(docs)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory=CHROMA_PATH
)

db.persist()
print(f"Ingested {len(chunks)} chunks from {len(pdf_files)} PDFs")

