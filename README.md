# 📄 Smart Chat with RAG (Retrieval-Augmented Generation)


A fully local **document question-answering system** that allows users to upload PDFs or text files and ask questions over their content using a **Retrieval-Augmented Generation (RAG)** pipeline.

This project runs **entirely offline**:
- Uses a local LLM, FAISS vector search, FastAPI backend, and Streamlit frontend

---

## 🚀 Features

- Upload **PDF** and **TXT** documents
- Paste raw text manually
- Ask questions about uploaded documents
- Get **grounded answers** based only on retrieved context
- Clear/reset documents and start fresh
- Fully local LLM inference (via `llama.cpp`)
- Simple local web UI built with Streamlit

---

##  How It Works

This project implements **Retrieval-Augmented Generation (RAG)**:

1. **Ingestion**
   - Uploaded documents are split into small text chunks
2. **Embedding**
   - Each chunk is converted into a vector embedding
3. **Retrieval**
   - FAISS retrieves the most relevant chunks for a query
4. **Generation**
   - A local LLM generates an answer using *only* the retrieved context

This prevents hallucinations and ensures answers are grounded in the documents.

---

## 🏗️ Architecture

User
↓
Streamlit UI
↓
FastAPI Backend
↓
RAG Pipeline
├── Chunking
├── Embeddings
├── FAISS Retrieval
└── Local LLM (llama.cpp)
↓
Answer


---

## ⚙️ Setup & Installation

###  Clone the repository

```bash
git clone <https://github.com/RaphSmart/smart-chat-rag>
cd doc-chat-rag
```

Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Download a local LLM
Place a compatible .gguf model (e.g. phi-2.gguf) inside:models/


## ▶️ Running the Project
### Start the FastAPI backend
```bash
uvicorn src.api.main:app --reload
```

### Start the Streamlit UI
```bash
streamlit run src/ui/app.py
```

Then open links in browser
```bash
UI: http://localhost:8501
API: http://localhost:8000/docs
```

## Docker with the app

docker build --no-cache -t smart_rag . 

### Run from consol
docker run -it --rm \
  -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  smart_rag \
  uvicorn src.api.main:app --host 0.0.0.0 --port 8000

## docker-compose with the app
```bash
docker-compose up
```