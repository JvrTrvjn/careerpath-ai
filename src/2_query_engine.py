# src/2_query_engine.py

import os
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

def main():
    """
    Función principal que orquesta el pipeline de RAG:
    1. Carga la API Key
    2. Define la pregunta
    3. Se conecta a la BD Vectorial
    4. Crea el embedding de la pregunta
    5. Busca chunks relevantes (Retrieval)
    6. Construye el prompt y genera una respuesta (Generation)
    """
    # 1. Cargar la API Key de forma segura
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API Key de Google no encontrada. Asegúrate de que tu archivo .env está correcto.")
    genai.configure(api_key=api_key)

    # 2. Definimos la pregunta del usuario
    user_query = "¿Qué habilidades necesito para ser Senior AI Engineer?"

    # --- FASE DE RECUPERACIÓN (RETRIEVAL) ---

    # 3. Cargamos el modelo de embeddings y nos conectamos a la BD
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="../chroma_db")
    collection = client.get_collection(name="career_path_docs")

    # 4. Convertimos la pregunta en un embedding
    query_embedding = embedding_model.encode(user_query).tolist()

    # 5. Buscamos los chunks más relevantes
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3 # Pedimos 3 chunks para tener más contexto
    )

    retrieved_chunks = results['documents'][0]

    # --- FASE DE GENERACIÓN (GENERATION) ---

    # 6. Construimos el prompt para el LLM
    prompt_template = """
    Eres un asistente de Recursos Humanos especializado en planes de carrera. 
    Tu objetivo es responder a la pregunta del usuario basándote ÚNICA Y EXCLUSIVAMENTE en el contexto que te proporciono.
    Si la información no está en el contexto, indica que no tienes suficiente información para responder.

    CONTEXTO:
    {context}

    PREGUNTA:
    {question}

    RESPUESTA:
    """

    context_for_prompt = "\n---\n".join(retrieved_chunks)

    final_prompt = prompt_template.format(
        context=context_for_prompt,
        question=user_query
    )

    # 7. Llamamos a Gemini para generar la respuesta
    print("Generando respuesta con Gemini...")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(final_prompt)

    # 8. Mostramos el resultado final
    print("\n--- PREGUNTA DEL USUARIO ---")
    print(user_query)
    print("\n--- RESPUESTA GENERADA POR LA IA ---")
    print(response.text)

if __name__ == "__main__":
    main()