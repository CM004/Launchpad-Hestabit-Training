import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)

loaded_docs = json.load(open("src/data/cleaned/documents.json"))

all_chunks = []

for doc in loaded_docs:
    text = doc["text"]
    source = doc["source"]
    
    chunks = splitter.split_text(text)
    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "text": chunk,
            "source": source,
            "chunk_id": i
        })
    print(source, "->", len(chunks), "chunks")

Path("src/data/chunks").mkdir(exist_ok=True)
open("src/data/chunks/chunks.json", "w").write(json.dumps(all_chunks, indent=2))
print("Total:", len(all_chunks), "chunks saved")
