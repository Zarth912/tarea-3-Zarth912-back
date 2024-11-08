# backend/main.py
import os
from fastapi import FastAPI, HTTPException
from .services import fill_database, retrieve_similar_fragments
from .llm_client import query_llm
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://llm-chatbot-ten.vercel.app"],  # Permite el frontend de React
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

@app.get("/")
async def read_root():
    return {"message": "Backend is running"}

class QueryRequest(BaseModel):
    question: str

@app.post("/query/")
async def query(query_request: QueryRequest):
    try:
        relevant_fragments = retrieve_similar_fragments(query_request.question)
        response = query_llm(query_request.question, relevant_fragments[:2048])
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Incluir esta parte solo cuando estás corriendo localmente
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000)) 
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)