import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Encuentra la ruta al archivo .env en el directorio raíz del proyecto
project_root = Path(__file__).parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Configura la API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API Key de Google no encontrada. Asegúrate de que tu archivo .env está en la raíz del proyecto.")
genai.configure(api_key=api_key)

print("--- Modelos Disponibles que soportan 'generateContent' ---")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)