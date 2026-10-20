
from rag.chunker import split_into_chunks

sample_text = """
Brand tone: Friendly and simple.
Required keyword: Reusable.
Avoid unsupported claims.
Primary colors: Green and white.
Never promise guaranteed results.
"""

chunks = split_into_chunks(
    sample_text,
    chunk_size=8,
    overlap=2
)

print("Chunking successful!")
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}:")
    print(chunk)
