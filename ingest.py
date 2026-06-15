import os

DOCUMENTS_DIR = "documents"

def load_documents():
    """Load all .txt files from the documents/ folder."""
    docs = []
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCUMENTS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw = f.read()
            cleaned = clean(raw)
            if cleaned:
                docs.append({"source": filename, "text": cleaned})
    print(f"Loaded {len(docs)} documents.")
    return docs

def clean(text):
    """Remove source headers and normalize whitespace."""
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # Skip source/header lines we added manually
        if line.startswith("SOURCE:") or line.startswith("PROFESSOR/TOPIC:") or line == "---":
            continue
        if line:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

if __name__ == "__main__":
    docs = load_documents()
    for doc in docs:
        print(f"\n=== {doc['source']} ===")
        print(doc['text'][:300])
        print("...")