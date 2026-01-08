from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
import sys
sys.path.append('src')
import uuid
import shutil
from pathlib import Path

from memory.memory_store import mem
from retriever.image_search import search_text, search_image
from generator.llm_client import generate_answer
from evaluation.rag_eval import evaluate_full

router = APIRouter()

@router.post("/ask/image")
async def ask_image(question: str = Form(...), image: UploadFile = File(None), session_id: str = Form(None)):
    session_id = session_id or str(uuid.uuid4())[:8]
    
    if image:
        temp_path = Path("src/temp") / image.filename  
        temp_path.parent.mkdir(exist_ok=True, parents = True)
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(image.file, f)
        images = search_image(str(temp_path), k=3)
        temp_path.unlink(missing_ok=True)
    else:
        images = search_text(question, k=3)
    
    context = "\n".join([f"{i+1}. {img['caption']}" for i, img in enumerate(images)])
    prompt = f"Based on these images:\n{context}\n\nQuestion: {question}\nAnswer:"
    answer = generate_answer(prompt)

    final_answer, confidence, safe = evaluate_full(question, answer, context, mem, session_id)

    mem.add(session_id, "user", question)
    mem.add(session_id, "bot", final_answer)

    return {
        "answer": final_answer, 
        "images": [f"{img['folder']}/{img['file']}" for img in images],
        "confidence": confidence,
        "safe": safe,
        "session_id": session_id,
        "history": mem.get(session_id)[-5:]
    }
