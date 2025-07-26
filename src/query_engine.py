import os
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pathlib import Path

# CORRECCIÓN: Calculamos la ruta raíz para que siempre funcione
project_root = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=project_root / ".env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# CORRECCIÓN: Usamos la ruta absoluta a la base de datos
client = chromadb.PersistentClient(path=str(project_root / "chroma_db"))
collection = client.get_collection(name="career_path_docs")
llm = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_rag_response(query: str) -> str:
    # ... (el resto de la función no cambia) ...
    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_chunks = results['documents'][0]
    context_for_prompt = "\n---\n".join(retrieved_chunks)

    prompt_template = """
    Eres un asistente de RRHH. Responde a la pregunta del usuario basándote solo en el siguiente contexto.
    Si la información no está en el contexto, di que no tienes suficiente información.

    CONTEXTO:
    {context}

    PREGUNTA:
    {question}

    RESPUESTA:
    """

    final_prompt = prompt_template.format(context=context_for_prompt, question=query)
    response = llm.generate_content(final_prompt)
    return response.text