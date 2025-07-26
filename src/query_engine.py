import os
import chromadb
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=project_root / ".env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=str(project_root / "chroma_db"))
collection = client.get_collection(name="career_path_docs")
llm = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_rag_response(query: str) -> str:
    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_chunks = results['documents'][0]
    context_for_prompt = "\n---\n".join(retrieved_chunks)

    prompt_template = """
    You are an HR assistant. Answer the user's question based only on the following context.
    If the information is not in the context, state that you do not have enough information.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """

    final_prompt = prompt_template.format(context=context_for_prompt, question=query)
    response = llm.generate_content(final_prompt)
    return response.text