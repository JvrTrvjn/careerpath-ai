from fastapi import FastAPI
from pydantic import BaseModel
from . import query_engine 
class QueryRequest(BaseModel):
    question: str

app = FastAPI(
    title="CareerPath AI API",
    description="API para el agente inteligente de planes de carrera.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de CareerPath AI"}

@app.post("/query")
def run_query(request: QueryRequest):
    """
    Recibe una pregunta y devuelve la respuesta generada por el sistema RAG.
    """
    response_text = query_engine.get_rag_response(query=request.question)
    return {"answer": response_text}