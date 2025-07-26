# src/1_data_ingestion.py

import pypdf
from pathlib import Path

def read_pdf(file_path: Path) -> str:
    """Lee el texto de un archivo PDF."""
    try:
        reader = pypdf.PdfReader(file_path)
        pdf_text = ""
        for page in reader.pages:
            pdf_text += page.extract_text()
        return pdf_text
    except Exception as e:
        print(f"Error leyendo el archivo {file_path}: {e}")
        return ""

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    # NOTA: Usamos Path para manejar las rutas de forma robusta, independientemente del sistema operativo.
    # '..' se refiere al directorio padre, así que salimos de 'src' para entrar en 'data'.
    data_path = Path("../data/senior_dev.txt") # Cambia esto al nombre de uno de tus archivos

    print(f"--- Leyendo el archivo: {data_path.name} ---")

    if data_path.suffix == ".pdf":
        content = read_pdf(data_path)
    elif data_path.suffix == ".txt":
        # .read_text() es una forma sencilla de leer archivos de texto
        content = data_path.read_text(encoding="utf-8")
    else:
        content = "Formato de archivo no soportado."

    print(content)
    print("\n--- Lectura finalizada ---")