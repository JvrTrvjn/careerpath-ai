import streamlit as st
from query_engine import get_rag_response

# --- Configuración de la Página ---
st.set_page_config(
    page_title="CareerPath AI",
    page_icon="🤖",
    layout="centered"
)

# --- Título y Descripción ---
st.title("🤖 CareerPath AI: Asesor de Carrera")
st.write(
    "Haz una pregunta sobre tu plan de carrera y la IA te responderá basándose "
    "en los documentos de la base de conocimiento."
)

# --- Input del Usuario ---
user_question = st.text_input("¿Cuál es tu pregunta?", "")

# --- Botón de Envío y Lógica Principal ---
if st.button("Obtener Respuesta"):
    if user_question:
        with st.spinner("Pensando... 🧠"):
            response = get_rag_response(user_question)
            st.success("¡Aquí tienes tu respuesta!")
            st.write(response)
    else:
        st.warning("Por favor, introduce una pregunta.")