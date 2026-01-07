import sys
sys.path.append('src')
from pipelines.context_builder import build_context
from generator.llm_client import generate_answer
from prompts.rag_prompt import get_rag_prompt

def retrieve_and_answer(query, k=5):

    result = build_context(query, k=k) #using day 2 hybrid retrieval + reranking
    
    prompt = get_rag_prompt(result['context'], query) #giving prompt using existing prompt template
    answer = generate_answer(prompt)
    
    sources = [(src['source'], "chunk:", src['chunk_id']) for src in result['sources']] #sources from context
    
    return answer, sources

if __name__ == "__main__":
    query = input("Ask: ")
    answer, sources = retrieve_and_answer(query)
    print("\nAnswer:", answer)
    print("\nSources:", set(sources))
