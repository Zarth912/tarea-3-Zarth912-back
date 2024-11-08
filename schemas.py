# backend/schemas.py
from pydantic import BaseModel
from typing import List

class ProcessScriptsResponse(BaseModel):
    embeddings: List[List[float]]

class QueryRequest(BaseModel):
    question: str
    script_fragments: List[str]

class QueryResponse(BaseModel):
    response: str