from src.embeddings.embedding_factory import EmbeddingFactory



embedding_model = EmbeddingFactory.get_embedding_model(
    "gemini"
)


product_text = """
Product ID: 101
Name: Aashirvaad Atta
Category: Grocery
Price: 280
Stock: 50
Location: Block A Rack 3
"""


vector = embedding_model.generate_embedding(
    product_text
)


print(len(vector))