import os
import glob
import re
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

env_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path=env_path)

MONGO_URL = os.getenv("MONGO_URL") or os.getenv("MANGODB_API_URL")

def clean_num(val):
    if pd.isna(val):
        return 0.0
    s = re.sub(r"[^\d.]", "", str(val))
    try:
        return float(s) if s else 0.0
    except ValueError:
        return 0.0

def sync_to_mongodb():
    print(f"Connecting to MongoDB Atlas: {MONGO_URL[:35]}...")
    client = MongoClient(MONGO_URL)
    db = client["department_store"]
    collection = db["products"]

    raw_files = glob.glob('data/raw/*.csv') + glob.glob('data/raw data/*.csv')
    if not raw_files:
        print("No CSV files found in data/raw/")
        return

    csv_path = raw_files[0]
    print(f"Reading dataset: {csv_path}")
    df = pd.read_csv(csv_path)

    # Clear existing documents
    collection.delete_many({})

    records = []
    for idx, row in df.iterrows():
        pid = str(row.get('Product ID', f"P{idx+1:05d}")).strip()
        record = {
            "product_id": pid,
            "name": str(row.get('Name', '')).strip(),
            "category": str(row.get('Category', '')).strip(),
            "brand": str(row.get('Brand', '')).strip(),
            "price": clean_num(row.get('Price/RS', row.get('Price', 0))),
            "expiry_date": str(row.get('Expiry Date', '')).strip(),
            "stock": int(clean_num(row.get('Stock Quantity', row.get('Stock', 0)))),
            "supplier_name": str(row.get('Supplier Name', '')).strip(),
            "supplier_phone": str(row.get('Supplier Ph No', '')).strip(),
            "supplier_email": str(row.get('Supplier Email', '')).strip(),
            "block_name": str(row.get('Block Name', 'A')).strip(),
            "rack_no": str(row.get('Rack No', '1')).strip(),
            "section": str(row.get('Session', row.get('Section', 'General'))).strip()
        }
        records.append(record)

    if records:
        res = collection.insert_many(records)
        print(f"Successfully inserted {len(res.inserted_ids)} documents into MongoDB Atlas!")

    total = collection.count_documents({})
    print(f"Verified collection 'department_store.products' document count: {total}")
    client.close()

if __name__ == "__main__":
    sync_to_mongodb()
