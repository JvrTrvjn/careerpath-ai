import chromadb
from sentence_transformers import SentenceTransformer

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    # 1. Definimos la pregunta del usuario
    user_query = "¿Qué necesito para ser Senior AI Engineer?"

    # 2. Cargamos el MISMO modelo de embeddings que usamos en la ingesta
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # 3. Nos conectamos a la base de datos que ya existe
    client = chromadb.PersistentClient(path="../chroma_db")
    collection = client.get_collection(name="career_path_docs")

    # 4. Convertimos la pregunta del usuario en un embedding
    query_embedding = embedding_model.encode(user_query).tolist()

    # 5. Realizamos la búsqueda por similitud en ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2 # Queremos que nos devuelva los 2 chunks más relevantes
    )

    # 6. Mostramos los resultados
    print(f"--- Pregunta ---")
    print(user_query)
    print("\n--- Resultados más relevantes de la Base de Datos ---")

    # Reemplaza esta parte en tu código

for doc in results['documents'][0]:
    # 1. Primero, limpiamos el texto y lo guardamos en una nueva variable
    cleaned_doc = doc.replace('\n', ' ')

    # 2. Luego, imprimimos la variable ya limpia
    print(f"- {cleaned_doc}")
    print("-" * 50)