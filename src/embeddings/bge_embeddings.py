from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

def get_embeddings(documents):

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    )

    return embeddings