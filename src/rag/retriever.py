import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="data/chromadb")
collection = client.get_or_create_collection(name="products")

# Initialize the embedding model for the query
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def retrieve(query):
    # Encode query to generate embedding
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    if results and results.get("documents"):
        return results["documents"][0]
    return []