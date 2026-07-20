import chromadb
from sentence_transformers import SentenceTransformer

_client = None
_collection = None
_model = None

def get_retriever_resources():
    global _client, _collection, _model
    if _client is None:
        _client = chromadb.PersistentClient(path="data/chromadb")
        _collection = _client.get_or_create_collection(name="products")
    if _model is None:
        _model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    return _collection, _model

def retrieve(query):
    collection, model = get_retriever_resources()
    # Encode query to generate embedding
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    if results and results.get("documents"):
        return results["documents"][0]
    return []