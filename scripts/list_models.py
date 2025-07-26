import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).parent.parent
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path=dotenv_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API Key not found. Make sure your .env file is in the project root.")
genai.configure(api_key=api_key)

print("--- Available Models supporting 'generateContent' ---")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)