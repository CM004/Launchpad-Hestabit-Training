from sentence_transformers import SentenceTransformer, util
import re
import sys
sys.path.append('src')
from generator.llm_client import generate_answer

model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_scores(question, answer, context):
    
    #encode once for efficiency
    q_emb = model.encode(question)
    a_emb = model.encode(answer)
    c_emb = model.encode(context)
    
    # 1. CONTEXT MATCH (question vs context)
    context_match = float(util.cos_sim(q_emb, c_emb).max().item())
    
    # 2. FAITHFULNESS (answer sentences vs context)
    faithfulness = float(util.cos_sim(a_emb, c_emb).max().item())
    
    # 3. ANSWER RELEVANCY (question vs answer)
    answer_relevancy = float(util.cos_sim(q_emb, a_emb).item())
    
    # 4. HALLUCINATION 
    hallucination = 1.0 - faithfulness
    
    # 5. CONFIDENCE (weighted)
    confidence = context_match * 0.25 + faithfulness * 0.25 + answer_relevancy * 0.5
    
    return {
        "context_match": float(context_match),
        "faithfulness": float(faithfulness),
        "answer_relevancy": float(answer_relevancy),
        "hallucination": float(hallucination),
        "confidence": float(confidence),
        "safe": True
    }

def evaluate_full(question, answer, context, mem, session_id):
    scores = calculate_scores(question, answer, context)
    
    # self refinement loop
    if scores["confidence"] < 0.5:
        mem.add(session_id, "system", f"Refining (confidence={scores['confidence']:.2f})")
        refined_prompt = f"Context: {context[:1000]}\nQ: {question}\nImprove: {answer[:200]}"
        answer = generate_answer(refined_prompt)
        scores = calculate_scores(question, answer, context)  #rescore
        mem.add(session_id, "system", "Refined answer")
    
    mem.add(session_id, "system", f"Evaluation: confidence={scores['confidence']:.2f}")
    return answer, scores["confidence"], scores["safe"]
