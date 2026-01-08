from fastapi import APIRouter
from pydantic import BaseModel
import sys
sys.path.append('src')
import uuid

from memory.memory_store import mem
from pipelines.sql_pipeline import run_sql_qa
from evaluation.rag_eval import evaluate_full

router = APIRouter()

class SQLRequest(BaseModel):
    question: str
    session_id: str = None

@router.post("/ask/sql")
def ask_sql(req: SQLRequest):
    session_id = req.session_id or str(uuid.uuid4())[:8]
    
    answer = run_sql_qa(req.question)
    
    context = f"SQL Question: {req.question}\nSQL Answer: {answer}"
    final_answer, confidence, safe = evaluate_full(req.question, answer, context, mem, session_id)

    mem.add(session_id, "user", req.question)
    mem.add(session_id, "bot", final_answer)

    return {
        "answer": final_answer,
        "confidence": confidence,
        "safe": safe,
        "session_id": session_id,
        "history": mem.get(session_id)[-5:]
    }
