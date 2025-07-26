# src/1_data_ingestion.py

import yaml
import pypdf
import pandas as pd
import chromadb
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# ... (las funciones load_config, read_pdf, read_documents_from_directory, y chunk_documents no cambian) ...
def load_config(config_path: str = "config.yaml") -> dict:
    project_root = Path(__file__).resolve().parent.parent
    with open(project_root / config_path, "r") as f:
        return yaml.safe_load(f)

def read_documents_from_directory(directory_path: Path) -> list[dict]:
    documents = []
    for file_path in directory_path.iterdir():
        if file_path.is_file():
            content = ""
            if file_path.suffix == ".txt":
                content = file_path.read_text(encoding="utf-8")
            elif file_path.suffix == ".pdf":
                content = pypdf.PdfReader(file_path).pages[0].extract_text()

            if content:
                documents.append({"source": file_path.name, "content": content})
    return documents

def chunk_documents(documents: list[dict]) -> list[dict]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = []
    for doc in documents:
        split_content = text_splitter.split_text(doc['content'])
        for i, chunk_text in enumerate(split_content):
            chunks.append({
                "source": doc['source'],
                "content": chunk_text,
                "chunk_id": f"{doc['source']}-{i}"
            })
    return chunks

def create_and_store_embeddings(chunks: list[dict]):
    """Crea embeddings y los almacena en ChromaDB."""
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Extraemos el contenido y los metadatos para ChromaDB
    contents = [chunk['content'] for chunk in chunks]
    metadatas = [{"source": chunk['source']} for chunk in chunks]
    ids = [chunk['chunk_id'] for chunk in chunks]

    # Generamos los embeddings
    print("\nGenerando embeddings...")
    embeddings = embedding_model.encode(contents, show_progress_bar=True)

    # Conectamos con ChromaDB y almacenamos los datos
    # ChromaDB creará una base de datos local en la carpeta 'chroma_db'
    client = chromadb.PersistentClient(path=str(project_root / "chroma_db"))
    collection_name = "career_path_docs"

    # Borramos la colección si ya existe, para empezar de cero cada vez
    if collection_name in [c.name for c in client.list_collections()]:
        client.delete_collection(name=collection_name)

    collection = client.create_collection(name=collection_name)

    print(f"Almacenando {len(chunks)} chunks en la colección '{collection_name}' de ChromaDB...")
    collection.add(
        embeddings=embeddings.tolist(),
        documents=contents,
        metadatas=metadatas,
        ids=ids
    )
    print("¡Almacenamiento completado!")

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    config = load_config()
    data_path_str = config['data_source']['path']
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / data_path_str

    raw_documents = read_documents_from_directory(data_dir)
    document_chunks = chunk_documents(raw_documents)

    # 4. Crear y almacenar los embeddings
    create_and_store_embeddings(document_chunks)