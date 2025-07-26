from fastapi import FastAPI

# 1. Crear una instancia de la aplicación FastAPI
app = FastAPI(
    title="CareerPath AI API",
    description="API para el agente inteligente de planes de carrera.",
    version="0.1.0",
)

# 2. Definir nuestro primer "endpoint" o ruta
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de CareerPath AI"}