import yaml
import pypdf
import pandas as pd
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_config(config_path: str = "config.yaml") -> dict:
    project_root = Path(__file__).resolve().parent.parent
    with open(project_root / config_path, "r") as f:
        return yaml.safe_load(f)

def read_pdf(file_path: Path) -> str:
    reader = pypdf.PdfReader(file_path)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

def read_documents_from_directory(directory_path: Path) -> list[dict]:
    documents = []
    for file_path in directory_path.iterdir():
        if file_path.is_file():
            content = ""
            if file_path.suffix == ".txt":
                content = file_path.read_text(encoding="utf-8")
            elif file_path.suffix == ".pdf":
                content = read_pdf(file_path)

            if content:
                # Cambiamos 'filename' por 'source' para más claridad
                documents.append({"source": file_path.name, "content": content})
    return documents

def chunk_documents(documents: list[dict]) -> list[dict]:
    """Divide el contenido de los documentos en chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # El tamaño máximo de cada chunk en caracteres
        chunk_overlap=200,    # El número de caracteres que se solapan entre chunks
        length_function=len,
    )

    chunks = []
    for doc in documents:
        split_content = text_splitter.split_text(doc['content'])
        for i, chunk_text in enumerate(split_content):
            chunks.append({
                "source": doc['source'],
                "content": chunk_text,
                "chunk_id": f"{doc['source']}-{i}" # Un ID único para cada chunk
            })
    return chunks

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    config = load_config()
    data_path_str = config['data_source']['path']
    project_root = Path(__file__).resolve().parent.parent
    data_dir = project_root / data_path_str

    # 1. Leer los documentos originales
    raw_documents = read_documents_from_directory(data_dir)
    print(f"Se han encontrado y procesado {len(raw_documents)} documentos.")

    # 2. Dividir los documentos en chunks
    document_chunks = chunk_documents(raw_documents)
    print(f"Los documentos se han dividido en {len(document_chunks)} chunks.")

    # 3. Crear el DataFrame final con los chunks
    df = pd.DataFrame(document_chunks)

    print("\n--- Información del DataFrame de Chunks ---")
    df.info()
    print("\n--- Ejemplo de un Chunk ---")
    # .to_markdown() es útil para una visualización limpia en la terminal
    print(df.head(1).to_markdown(index=False))