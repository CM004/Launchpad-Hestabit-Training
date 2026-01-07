import sys
sys.path.append('src')
from retriever.hybrid_retriever import retrieve
from retriever.reranker import rerank

def build_context(query, k=5):
    docs = retrieve(query, k=50)
    reranked = rerank(query, docs, top_k=k)
    context = "\n\n".join([f"[{i+1}] {d.page_content}" for i, d in enumerate(reranked)])
    return {
        "context": context,
        "sources": [{"source": d.metadata["source"], "chunk_id": d.metadata["chunk_id"]}
        for d in reranked]}

if __name__ == "__main__":
    query = input("Enter your query: ")
    k = 5
    
    print("\nRetrieving and reranking...\n")
    result = build_context(query, k=k)
    
    print("CONTEXT")
    print("\n" + result["context"])

    print("SOURCES", len(result['sources']), "chunks)")
    for i, source in enumerate(result["sources"], 1):
        print(f"{i}. {source}")