# backend/vector_store.py
import faiss
import numpy as np

embedding_dim = 768
index = faiss.IndexFlatL2(embedding_dim)
fragments = []

def store_embedding(fragment_id: str, embedding: list, fragment: str):
    """Almacena el embedding y su fragmento correspondiente en la base de datos."""
    global fragments
    np_embedding = np.array([embedding], dtype=np.float32)
    index.add(np_embedding)
    fragments.append((fragment_id, fragment))
    print(f"Embedding de fragmento {fragment_id} almacenado en la base de datos.")

def search_similar(query_embedding: list, top_k: int = 5) -> list:
    """Realiza una búsqueda de similitud para el embedding de la consulta."""
    _, indices = index.search(np.array([query_embedding], dtype=np.float32), top_k)
    return [fragments[i][1] for i in indices[0]]