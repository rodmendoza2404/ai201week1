import chromadb
from sentence_transformers import SentenceTransformer
from chunk import get_all_chunks

COLLECTION_NAME = "fiu_cs_guide"

def build_vector_store():
    chunks = get_all_chunks()
    print(f"Embedding {len(chunks)} chunks...")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection if rebuilding
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass
    
    collection = client.create_collection(COLLECTION_NAME)
    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
        ids=[f"{c['source']}_{c['chunk_index']}" for c in chunks]
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB.")

if __name__ == "__main__":
    build_vector_store()