FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

RUN pip install --upgrade pip

# Install torch CPU
RUN pip install --no-cache-dir \
    torch==2.4.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Install all other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download embedding model AFTER install
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy source code
COPY src ./src
COPY README.md .

EXPOSE 8000
EXPOSE 8501

CMD ["bash"]

