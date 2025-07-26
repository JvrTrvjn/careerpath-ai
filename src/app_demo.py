import streamlit as st
from query_engine import get_rag_response

# --- Configuración de la Página ---
st.set_page_config(
    page_title="CareerPath AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 CareerPath AI: Career Advisor")
st.write(
    "Ask a question about your career path and the AI will answer based "
    "on the knowledge base documents."
)

user_question = st.text_input("What is your question?", "")

if st.button("Get Answer"):
    if user_question:
        with st.spinner("Thinking... 🧠"):
            response = get_rag_response(user_question)
            st.success("Here is your answer!")
            st.write(response)
    else:
        st.warning("Please enter a question.")