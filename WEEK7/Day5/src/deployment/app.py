import sys
sys.path.append('src')
from fastapi import FastAPI
from routes import ask, ask_sql, ask_image

app = FastAPI()

app.include_router(ask.router)
app.include_router(ask_sql.router)
app.include_router(ask_image.router)

@app.get("/")
def home():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
