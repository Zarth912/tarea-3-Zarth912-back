# backend/llm_client.py
import requests
from typing import List

def query_llm(question: str, context_fragments: List[str]) -> str:
    url = "http://tormenta.ing.puc.cl/api/llm"
    context = " ".join(context_fragments)
    payload = {
        "model": "integra-LLM",
        "prompt": f"Contexto:\n{context}\nPregunta: {question}"
    }
    headers = {"Authorization": "Bearer <tu_token_aqui>"}  # Asegúrate de agregar tu token

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        raise Exception(f"Error en la consulta al LLM: {response.status_code} - {response.text}")