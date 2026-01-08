# **Day 5 Deployment Notes**

## **Architecture**
```
FastAPI → FAISS/SQL/Image rag pipeline → Evaluator → Memory (CHAT-LOGS.json)
```

## **Endpoints**
```bash
/ask        # Text RAG (FAISS)
curl -X POST http://localhost:8000/ask -d '{"question": "who is the ceo of ACRES"}'

![alt text](<Screenshot from 2026-01-08 17-26-26.png>)

![alt text](<Screenshot from 2026-01-08 17-26-32.png>)

/ask/sql    # Chinook SQL  
curl -X POST http://localhost:8000/ask/sql -d '{"question": "highest sales of each genre"}'

![alt text](<Screenshot from 2026-01-08 15-53-11.png>)

/ask/image  # Image RAG (CLIP-BLIP)
curl -X POST "http://localhost:8000/ask/image" -F "question=construction"

![alt text](<Screenshot from 2026-01-08 17-41-00.png>)

![alt text](<Screenshot from 2026-01-08 17-36-43.png>)

![alt text](<Screenshot from 2026-01-08 17-36-50.png>) 

```

## **Response:**
```json
{"answer": "...", "confidence": 0.85, "safe": true, "session_id": "abc123", "history": [...]}
```

![alt text](<Screenshot from 2026-01-08 17-37-31.png>) 
![alt text](<Screenshot from 2026-01-08 17-35-05.png>) 
![alt text](<Screenshot from 2026-01-08 17-34-31.png>)
![alt text](<Screenshot from 2026-01-08 17-45-11.png>) 

## **Evaluator** (`rag_eval.py`)
```
confidence = 0.25×context + 0.25×faithfulness + 0.5×relevancy
if conf < 0.5 → self-refine → "Refining (conf=0.38)" → Re-score
```

## **Memory** (`memory_store.py`)
- Last 5 messages per session
- `src/logs/CHAT-LOGS.json` 
- Client sends `session_id` to continue with same session

![alt text](<Screenshot from 2026-01-08 17-44-11.png>)

![alt text](<Screenshot from 2026-01-08 17-44-30.png>)

## **Run**
```bash
python src/deployment/app.py
```
## **Files**
- Day5/
  - src/
    - deployment/app.py              
    - evaluation/rag_eval.py         
    - memory/memory_store.py         
    - routes/
      - ask.py                     
      - ask_sql.py                  
      - ask_image.py                
    - logs/CHAT-LOGS.json  

