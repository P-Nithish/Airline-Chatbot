import os
from pymongo import MongoClient
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        from langchain_community.document_loaders import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from .chroma_setup import get_chroma_client

load_dotenv()

MONGO_URI = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

def load_policy_docs_to_chroma():
    """Fetch policy docs from MongoDB and insert into Chroma vector store."""
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db["policies"]  # assume your collection name

    docs = list(collection.find({}))
    if not docs:
        print("No documents found in MongoDB.")
        return

    vectordb = get_chroma_client()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)

    for doc in docs:
        source = doc.get("source", "unknown")
        content = doc.get("content", "")
        if not content.strip():
            continue

        chunks = text_splitter.split_text(content)
        metadatas = [{"source": source, "doc_id": str(doc.get("_id"))} for _ in chunks]
        vectordb.add_texts(texts=chunks, metadatas=metadatas)

    vectordb.persist()
    print(f"Indexed {len(docs)} documents into Chroma.")
