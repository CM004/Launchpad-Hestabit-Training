from fastapi import APIRouter
from pydantic import BaseModel
import sys
sys.path.append('src')
import uuid
import math

from memory.memory_store import mem
from retriever.query_engine import retrieve_and_answer
from pipelines.context_builder import build_context
from evaluation.rag_eval import evaluate_full

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    session_id: str = None

@router.post("/ask")
def ask(req: AskRequest):
    session_id = req.session_id or str(uuid.uuid4())[:8]
    
    # Get answer (returns tuple)
    answer, sources = retrieve_and_answer(req.question)
    
    # Get context separately
    context_result = build_context(req.question)
    context = context_result['context']
    
    # evaluation
    final_answer, confidence, safe = evaluate_full(req.question, answer, context, mem, session_id)
    
    # Save to memory
    mem.add(session_id, "user", req.question)
    mem.add(session_id, "bot", final_answer)

    return {
        "answer": final_answer,
        "sources": sources,
        "confidence": confidence,
        "safe": safe,
        "session_id": session_id,
        "history": mem.get(session_id)[-5:]
    }
