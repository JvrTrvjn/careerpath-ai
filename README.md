# 🤖 CareerPath AI: Intelligent Career Advisor

CareerPath AI is a conversational agent built on a RAG (Retrieval-Augmented Generation) architecture. It answers questions about career development plans based on an internal, document-based knowledge base.

This project demonstrates a complete, end-to-end AI pipeline, from data ingestion and vector storage to exposing the logic via a RESTful API and an interactive web demo.

## ✨ Features

-   **Document Ingestion:** Processes `.txt` and `.pdf` files to build the knowledge base.
-   **Semantic Search:** Uses `sentence-transformers` for embeddings and a `ChromaDB` vector database to find the most relevant information.
-   **Context-Aware Generation:** Leverages Google's `Gemini` to generate accurate answers based *only* on the retrieved context.
-   **Professional API:** Exposes the RAG logic via a robust and auto-documented API built with `FastAPI`.
-   **Interactive Demo:** Includes a user-friendly web interface built with `Streamlit`.

## 🛠️ Tech Stack

-   **AI & MLOps:** PyTorch, Sentence-Transformers, LangChain, Google Generative AI, ChromaDB
-   **Backend:** FastAPI, Uvicorn
-   **Demo:** Streamlit
-   **Core:** Python, Pandas
-   **Tools:** Git

## 🚀 Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jtrevijano/careerpath-ai.git
    cd careerpath-ai
    ```

2.  **Create and activate the virtual environment:**
    ```bash
    python3 -m venv src/venv
    source src/venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```

4.  **Configure API Key:**
    -   Create a `.env` file in the project root.
    -   Add your favorite AI Studio key: `GOOGLE_API_KEY="your_key_here"`

## 🏃 Usage

**1. Build the Knowledge Base (Run once or to update):**
-   Add your `.txt` or `.pdf` documents to the `/data` folder.
-   Run the ingestion script:
    ```bash
    python3 src/data_ingestion.py
    ```

**2. Run the API Server:**
```bash
uvicorn src.main_api:app --reload
