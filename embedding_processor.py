# backend/embeddings_processor.py
import requests
from typing import List

def generate_embedding(text: str) -> List[float]:
    """Genera un embedding para el texto dado usando la API de embeddings."""
    url = "http://tormenta.ing.puc.cl/api/embed"
    payload = {
        "model": "nomic-embed-text",
        "input": text
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("embeddings", [])[0]
    else:
        raise Exception(f"Error {response.status_code} al obtener embedding: {response.text}")