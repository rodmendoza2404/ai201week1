import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

COLLECTION_NAME = "fiu_cs_guide"
TOP_K = 5

_model = None
_collection = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path="./chroma_db")
        _collection = client.get_collection(COLLECTION_NAME)
    return _collection

def retrieve(query, k=TOP_K):
    model = get_model()
    query_embedding = model.encode([query])[0].tolist()
    collection = get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )
    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": meta["source"],
            "distance": round(dist, 3)
        })
    return chunks

def ask(question):
    chunks = retrieve(question)
    
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n\n"
    
    sources = list(dict.fromkeys(c["source"] for c in chunks))  # deduplicated

    prompt = f"""You are a helpful assistant for FIU Computer Science students.
Answer the question using ONLY the information in the documents below.
If the documents do not contain enough information to answer, say exactly: "I don't have enough information on that topic in my documents."
Always end your answer by listing which sources you used.

Documents:
{context}

Question: {question}

Answer:"""

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600
    )
    
    answer = response.choices[0].message.content.strip()
    return {"answer": answer, "sources": sources, "chunks": chunks}

if __name__ == "__main__":
    test_queries = [
        "What do students say about Mark Weiss's exams?",
        "Is taking CDA 3102 and COP 3530 in the same semester a bad idea?",
        "Which CS professors at FIU do students recommend?"
    ]
    for q in test_queries:
        print(f"\nQ: {q}")
        result = ask(q)
        print(f"A: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print(f"Retrieved chunks (distances): {[c['distance'] for c in result['chunks']]}")