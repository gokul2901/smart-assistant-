import os
import chromadb
from ingestion.create_document import documents
from ingestion.embedding import embeddings

client = chromadb.PersistentClient(path="data/chromadb")

collection = client.get_or_create_collection("products")

# Generate unique IDs for all documents
ids = [str(i) for i in range(len(documents))]

print(f"Adding {len(documents)} documents to collection 'products'...")
collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist()
)
print("Ingestion complete!")