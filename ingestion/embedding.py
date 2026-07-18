from sentence_transformers import SentenceTransformer
from ingestion.create_document import documents

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

embeddings = model.encode(documents)

if __name__ == "__main__":
    print(embeddings.shape)




#   Documents
#      ↓
# BGE Embedding Model
#      ↓
# Vectors
#      ↓
# Ready for ChromaDB Storage
