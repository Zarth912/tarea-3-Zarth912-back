# backend/services.py
import os
import re
from .vector_store import store_embedding, search_similar
from .embedding_processor import generate_embedding


FRAGMENT_SIZE = 500
SCRIPT_FOLDER = "./scripts/"  # Asegúrate de que esta ruta sea correcta

def clean_text(text: str) -> str:
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ,.?!\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_script_into_fragments(text: str, fragment_size: int = FRAGMENT_SIZE) -> list:
    words = text.split()
    fragments = [" ".join(words[i:i + fragment_size]) for i in range(0, len(words), fragment_size)]
    return fragments

def process_and_store_script(script_text: str, script_id: str, max_retries: int = 3):
    clean_script_text = clean_text(script_text)
    fragments = split_script_into_fragments(clean_script_text)
    total_fragmentos = len(fragments)  # Calcula el total de fragmentos

    for i, fragment in enumerate(fragments):
        fragment_id = f"{script_id}_{i}"
        attempt = 0
        while attempt < max_retries:
            try:
                embedding = generate_embedding(fragment)
                store_embedding(fragment_id, embedding, fragment)
                print(f"Fragmento {script_id} :{i + 1}/{total_fragmentos} almacenado correctamente.")
                break  # Sale del bucle si se almacena con éxito
            except Exception as e:
                attempt += 1
                print(f"Error al generar y almacenar embedding para fragmento {i + 1} del guion {script_id} (Intento {attempt}/{max_retries}): {e}")
                if attempt >= max_retries:
                    print(f"Fragmento {script_id} :{i + 1}/{total_fragmentos} omitido después de {max_retries} intentos fallidos.")

def fill_database():
    for filename in os.listdir(SCRIPT_FOLDER):
        if filename.endswith(".txt"):
            script_path = os.path.join(SCRIPT_FOLDER, filename)
            with open(script_path, "r", encoding="utf-8") as file:
                script_text = file.read()
                script_id = filename.split(".")[0]
                print(f"Procesando guion: {script_id}")
                process_and_store_script(script_text, script_id)

def retrieve_similar_fragments(query: str, top_k: int = 5) -> list:
    query_embedding = generate_embedding(query)
    similar_fragments = search_similar(query_embedding, top_k)
    if not similar_fragments:
        print("No se encontraron fragmentos relevantes para la pregunta.")
    return similar_fragments or []

if __name__ == "__main__":
    print("Iniciando llenado de base de datos...")
    fill_database()
    print("Llenado de base de datos completado.")