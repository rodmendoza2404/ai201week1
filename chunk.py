from ingest import load_documents

CHUNK_SIZE = 400
OVERLAP = 80

def chunk_text(text, source):
    """Split text into overlapping chunks of CHUNK_SIZE characters."""
    chunks = []
    start = 0
    chunk_index = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if len(chunk) > 50:  # skip tiny fragments
            chunks.append({
                "text": chunk,
                "source": source,
                "chunk_index": chunk_index
            })
            chunk_index += 1
        start += CHUNK_SIZE - OVERLAP
    return chunks

def get_all_chunks():
    docs = load_documents()
    all_chunks = []
    for doc in docs:
        chunks = chunk_text(doc["text"], doc["source"])
        all_chunks.extend(chunks)
    return all_chunks

if __name__ == "__main__":
    chunks = get_all_chunks()
    print(f"\nTotal chunks: {len(chunks)}")
    print("\n--- Sample chunks ---")
    for i, chunk in enumerate(chunks[:5]):
        print(f"\n[Chunk {i} | source: {chunk['source']}]")
        print(chunk['text'])
        print()