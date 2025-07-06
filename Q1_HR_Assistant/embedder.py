import chromadb
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection("hr_docs")

def embed_and_store(chunks, filename):
    embeddings = model.encode(chunks).tolist()
    metadata = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]
    ids = [f"{filename}_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, metadatas=metadata, ids=ids)

def query_similar(text, top_k=5):
    query_embedding = model.encode([text])[0].tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results
