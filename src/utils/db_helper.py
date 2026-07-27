import os
import glob
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

def get_csv_path():
    raw_files = glob.glob('data/raw/*.csv') + glob.glob('data/raw data/*.csv')
    if raw_files:
        return raw_files[0]
    return "data/raw/Departmental_Store_Inventorylist.xlsx - Store Inventory.csv"

CSV_PATH = get_csv_path()
CHROMA_PATH = "data/chromadb"
COLLECTION_NAME = "products"
MODEL_NAME = "BAAI/bge-small-en-v1.5"

def load_products_df():
    """Load products from CSV."""
    path = get_csv_path()
    if not os.path.exists(path):
        raise FileNotFoundError(f"Products CSV file not found at {path}")
    return pd.read_csv(path)

def save_products_df(df):
    """Save products DataFrame to CSV."""
    path = get_csv_path()
    df.to_csv(path, index=False)

def reindex_chromadb():
    """Rebuild ChromaDB collection using current CSV data."""
    df = load_products_df()
    
    documents = []
    ids = []
    
    for idx, row in df.iterrows():
        pid = str(row.get('Product ID', f"P{idx+1:05d}")).strip()
        name = str(row.get('Name', '')).strip()
        category = str(row.get('Category', '')).strip()
        brand = str(row.get('Brand', '')).strip()
        price = str(row.get('Price/RS', row.get('Price', ''))).strip()
        expiry = str(row.get('Expiry Date', '')).strip()
        stock = str(row.get('Stock Quantity', row.get('Stock', ''))).strip()
        supplier = str(row.get('Supplier Name', row.get('Supplier', ''))).strip()
        block = str(row.get('Block Name', 'A')).strip()
        rack = str(row.get('Rack No', '1')).strip()
        session = str(row.get('Session', row.get('Section', 'General'))).strip()
        
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
        ids.append(pid if pid else str(idx))
    
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(documents).tolist()
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
        
    collection = client.get_or_create_collection(COLLECTION_NAME)
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )
    print(f"Re-indexed {len(documents)} products in mongodb")

if __name__ == "__main__":
    reindex_chromadb()
