import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

CSV_PATH = "data/raw data/products.csv"
CHROMA_PATH = "data/chromadb"
COLLECTION_NAME = "products"
MODEL_NAME = "BAAI/bge-small-en-v1.5"

def load_products_df():
    """Load products from CSV."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Products CSV file not found at {CSV_PATH}")
    return pd.read_csv(CSV_PATH)

def save_products_df(df):
    """Save products DataFrame to CSV."""
    df.to_csv(CSV_PATH, index=False)

def reindex_chromadb():
    """Rebuild ChromaDB collection using the current contents of the CSV file."""
    df = load_products_df()
    
    # Compile documents including all features
    documents = []
    ids = []
    
    for idx, row in df.iterrows():
        # Clean data and handle NaNs
        pid = str(row.get('Product ID', '')).strip()
        name = str(row.get('Name', '')).strip()
        category = str(row.get('Category', '')).strip()
        brand = str(row.get('Brand', '')).strip()
        price = str(row.get('Price/RS', '')).strip()
        expiry = str(row.get('Expiry Date', '')).strip()
        stock = str(row.get('Stock Quantity', '')).strip()
        supplier = str(row.get('Supplier', '')).strip()
        block = str(row.get('Block Name', '')).strip()
        rack = str(row.get('Rack No', '')).strip()
        session = str(row.get('Session', '')).strip()
        
        doc = f"""
        Product ID: {pid}
        Product Name: {name}
        Category: {category}
        Brand: {brand}
        Price/RS: {price}
        Expiry Date: {expiry}
        Stock Quantity: {stock}
        Supplier: {supplier}
        Location: Block {block}, Rack {rack}, Section {session}
        """.strip()
        
        documents.append(doc)
        # Use Product ID or index as Chroma ID
        ids.append(pid if pid else str(idx))
    
    # Initialize SentenceTransformer
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(documents).tolist()
    
    # Initialize Chroma PersistentClient
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # Reset/delete the collection if it exists to ensure freshness
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
        
    collection = client.get_or_create_collection(COLLECTION_NAME)
    
    # Add to collection
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )
    print(f"Re-indexed {len(documents)} products in ChromaDB.")
