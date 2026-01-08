from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import json
from pathlib import Path

print("Loading chunks...")
chunks = json.load(open("src/data/chunks/chunks.json")) #load chunks
texts = [c["text"] for c in chunks]
metadatas = [{"source": c["source"], "chunk_id": c["chunk_id"]} for c in chunks] 
print("Loaded ",len(texts)," chunks")

print("Building BM25 index...")
bm25 = BM25Retriever.from_texts(texts, metadatas=metadatas) #BM25 retriever
bm25.k = 25
print("BM25 ready")

#print("Loading embedding model and building FAISS index...")
#embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", show_progress=True)
#langchain FAISS retriever
#faiss_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

faiss_path = Path("src/vectorstore/faiss_langchain")
if faiss_path.exists():
    print("Loading saved FAISS embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    faiss_store = FAISS.load_local("src/vectorstore/faiss_langchain", embeddings, allow_dangerous_deserialization=True)
    print("FAISS loaded")
else:
    print("Loading embedding model and building FAISS index (first time)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", show_progress=True)
    faiss_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    faiss_store.save_local("src/vectorstore/faiss_langchain")
    print("FAISS built and saved")

faiss = faiss_store.as_retriever(search_kwargs={"k": 25})
print("FAISS ready\n")

# print("Saving FAISS with metadata...")
# faiss_store.save_local("src/vectorstore/faiss_langchain")

def retrieve(query, k=5):
    bm25_docs = bm25.invoke(query)
    faiss_docs = faiss.invoke(query)
    
    scores = {}
    for rank, doc in enumerate(bm25_docs + faiss_docs):
        content = doc.page_content
        scores[content] = scores.get(content, 0) + 1/(rank+60)
    
    doc_map = {d.page_content: d for d in bm25_docs + faiss_docs}
    return [doc_map[c] for c in sorted(scores, key=scores.get, reverse=True)][:k]
