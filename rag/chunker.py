
def split_into_chunks(text, chunk_size=120, overlap=20):
    """
    Split text into word-based chunks.

    chunk_size: maximum words in each chunk
    overlap: words shared between consecutive chunks
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be >= 0 and smaller than chunk_size."
        )

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks
