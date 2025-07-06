from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def store_embeddings(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [c['text'] for c in chunks]
    vectors = model.encode(texts)
    
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors))
    
    return index, vectors, texts, chunks
