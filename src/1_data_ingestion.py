# src/1_data_ingestion.py

import yaml
import pypdf
import pandas as pd
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

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
                content = pypdf.PdfReader(file_path).pages[0].extract_text() # Simplificado para un PDF simple

            if content:
                documents.append({"source": file_path.name, "content": content})
    return documents

def chunk_documents(documents: list[dict]) -> list[dict]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
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

def create_embeddings(chunks_df: pd.DataFrame) -> pd.DataFrame:
    """Crea embeddings para el contenido de los chunks."""
    # Elegimos un modelo de embedding eficiente y multilingüe
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    # Convertimos la columna de contenido a una lista para el modelo
    corpus = chunks_df["content"].tolist()

    # Generamos los embeddings
    print("\nGenerando embeddings... (la primera vez puede tardar en descargar el modelo)")
    embeddings = embedding_model.encode(corpus, show_progress_bar=True)

    # Añadimos los embeddings como una nueva columna al DataFrame
    chunks_df["embedding"] = embeddings.tolist()
    return chunks_df

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    config = load_config()
    data_path_str = config['data_source']['path']
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / data_path_str

    raw_documents = read_documents_from_directory(data_dir)
    document_chunks = chunk_documents(raw_documents)
    df = pd.DataFrame(document_chunks)

    # 4. Crear los embeddings
    df_with_embeddings = create_embeddings(df)

    print("\n--- Información del DataFrame con Embeddings ---")
    df_with_embeddings.info()
    print("\n--- Verificando un Embedding ---")
    # Imprimimos la longitud del primer vector de embedding para confirmar
    print(f"El primer chunk tiene un vector de embedding con {len(df_with_embeddings.iloc[0]['embedding'])} dimensiones.")