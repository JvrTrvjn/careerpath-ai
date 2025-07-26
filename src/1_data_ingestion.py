# src/1_data_ingestion.py

import yaml
import pypdf
import pandas as pd
from pathlib import Path

def load_config(config_path: str = "config.yaml") -> dict:
    """Carga la configuración desde un archivo YAML."""
    # Vamos a la raíz del proyecto para encontrar el config.yaml
    project_root = Path(__file__).parent.parent
    with open(project_root / config_path, "r") as f:
        return yaml.safe_load(f)

def read_pdf(file_path: Path) -> str:
    # (Esta función no cambia)
    reader = pypdf.PdfReader(file_path)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

def read_documents_from_directory(directory_path: Path) -> list[dict]:
    # (Esta función no cambia)
    documents = []
    print(f"Buscando documentos en: {directory_path.resolve()}")
    for file_path in directory_path.iterdir():
        if file_path.is_file():
            if file_path.suffix == ".txt":
                content = file_path.read_text(encoding="utf-8")
                documents.append({"filename": file_path.name, "content": content})
            elif file_path.suffix == ".pdf":
                content = read_pdf(file_path)
                documents.append({"filename": file_path.name, "content": content})
    return documents

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    config = load_config()
    # Obtenemos la ruta desde el archivo de configuración
    data_path_str = config['data_source']['path']

    # Construimos la ruta completa desde la raíz del proyecto
    project_root = Path(__file__).parent.parent
    data_dir = project_root / data_path_str

    raw_documents = read_documents_from_directory(data_dir)

    df = pd.DataFrame(raw_documents)

    print(f"\nSe han encontrado y procesado {len(raw_documents)} documentos.")
    print("\n--- Información del DataFrame Creado ---")
    df.info()