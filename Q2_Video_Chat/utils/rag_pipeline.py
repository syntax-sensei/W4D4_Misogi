from openai import OpenAI
import numpy as np
import os

def seconds_to_timestamp(seconds):
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

def retrieve(query, index, texts, chunks, model):
    query_vector = model.encode([query])[0]
    D, I = index.search(np.array([query_vector]), k=3)

    top_chunks = [chunks[i] for i in I[0]]
    # Use readable timestamps in MM:SS format
    context = '\n'.join([f"[{seconds_to_timestamp(c['start'])} - {seconds_to_timestamp(c['end'])}] {c['text']}" for c in top_chunks])
    return context, top_chunks

def answer_question(context, question):
    # Check if OpenAI API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return "❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
    
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""Based on the following lecture content, answer the question.

Lecture Content:
{context}

Question: {question}

Please provide a clear and concise answer based only on the lecture content provided:"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on lecture content. Only use the information provided in the lecture content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"❌ Error generating answer: {str(e)}"
