from typing import List

def chunk_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Full document text
        chunk_size: Number of characters per chunk
        overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

        if start < 0:
            start = 0

    return chunks