from openai import OpenAI
import os
from embedder import query_similar
from utils import categorize_query
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(query):
    category = categorize_query(query)
    results = query_similar(query)

    context = "\n\n".join(results['documents'][0])
    references = results['metadatas'][0]

    prompt = f"""You are an HR assistant. Use the following HR policy context to answer the question. 
If unsure, say you don't know. Always cite document source at the end.

Context:
{context}

Question: {query}
Answer:"""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = completion.choices[0].message.content.strip()
    sources = ", ".join(set([f"{ref['source']} (Chunk {ref['chunk_index']})" for ref in references]))
    return answer, sources
