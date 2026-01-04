import json
import faiss
from sentence_transformers import SentenceTransformer
import sys
sys.path.append('src')
from generator.llm_client import generate_answer
from prompts.rag_prompt import get_rag_prompt

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("src/vectorstore/index.faiss")
chunks = json.load(open("src/vectorstore/metadata.json"))

def retrieve_and_answer(query, k=3):
    query_emb = model.encode([query]).astype('float32')
    _, idxs = index.search(query_emb, k)
    
    context = ""
    sources = []
    for i in idxs[0]:
        chunk = chunks[i]
        context += f"{chunk['text']}\n\n"
        sources.append((chunk['source'], "chunk:", chunk['chunk_id']))

    prompt = get_rag_prompt(context, query)
    answer = generate_answer(prompt)
    
    return answer, sources

if __name__ == "__main__":
    query = input("Ask: ")
    answer, sources = retrieve_and_answer(query)
    print("\nAnswer:", answer)
    print("\nSources:", set(sources))
