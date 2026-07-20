import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROK_API_KEY = os.getenv("GROK_API_KEY")
MIST_API_KEY = os.getenv("MIST_API_KEY")

# ChromaDB Path
CHROMA_DB_PATH = "data/chromadb"

# CSV File Path
CSV_FILE_PATH = "data/raw/products.csv"

# Collection Name
COLLECTION_NAME = "products"

# Retrieval Settings
TOP_K = 3