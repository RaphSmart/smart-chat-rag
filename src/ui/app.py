import streamlit as st
import requests
from pypdf import PdfReader

# Code below is add to activate clear button
if "docs_input" not in st.session_state:
    st.session_state.docs_input = ""

if "question" not in st.session_state:
    st.session_state.question = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

# End of code

# helper func for clear
def clear_all():
    st.session_state.docs_input = ""
    st.session_state.question = ""
    st.session_state.answer = ""
    st.success("Cleared. You can now add new documents.")

# pdf file upload
def read_uploaded_file(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")

    elif file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    return ""
# end pdf upload

API_BASE_URL = "http://localhost:8000"


st.set_page_config(page_title="Smart RAG Chat", layout="centered")

st.title("Smart RAG Chat")
st.write("Ask questions over your documents using a local LLM.")


# Document input
st.subheader("Ingest documents")


docs_input = st.text_area(
    "Paste one or more documents (separated by ---)",
    height=200,
    placeholder="Paste text here...\n\n---\n\nAnother document...",
    key="docs_input"
)

# file upload
uploaded_files = st.file_uploader(
    "Upload text files (.txt or .pdf)",
    type=["txt", "pdf"],
    accept_multiple_files=True
)

# Clear button
col1, col2 = st.columns([3, 1])

with col1:
    ingest_clicked = st.button("📥 Ingest Documents")

with col2:
    st.button("🧹 Clear", on_click=clear_all)


# Handle ingest
if ingest_clicked:
    docs = []

    # Uploaded files (TXT + PDF)
    if uploaded_files:
        for file in uploaded_files:
            content = read_uploaded_file(file)
            if content.strip():
                docs.append(content)

    # Pasted text
    pasted_docs = [
        d.strip()
        for d in st.session_state.docs_input.split("---")
        if d.strip()
    ]
    docs.extend(pasted_docs)

    if not docs:
        st.warning("Please upload or paste at least one document.")
    else:
        response = requests.post(
            f"{API_BASE_URL}/ingest",
            json={"documents": docs}
        )

        if response.status_code == 200:
            st.success("Documents ingested successfully!")
        else:
            st.error("Failed to ingest documents.")


# Query section
st.subheader("Ask a question")

question = st.text_input(
    "Your question",
    key="question"
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        response = requests.post(
            f"{API_BASE_URL}/query/",
            json={"question": question}
        )

        if response.status_code == 200:
            answer = response.json()["answer"]
            st.markdown("### Answer")
            st.write(answer)
        else:
            st.error("Failed to get an answer.")