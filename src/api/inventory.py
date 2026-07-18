# src/api/inventory.py

import pandas as pd
from fastapi import APIRouter

router = APIRouter()

def load_latest_products():
    try:
        from src.utils.db_helper import load_products_df
        df_latest = load_products_df()
    except Exception:
        from ingestion.csv_loader import load_csv
        df_latest = load_csv()
        
    latest_products = []
    latest_products_by_id = {}
    
    for _, row in df_latest.iterrows():
        pid = str(row["Product ID"]).strip()
        name = str(row["Name"]).strip()
        # Handle possible NaN values in Stock Quantity
        stock_val = row["Stock Quantity"]
        stock = int(stock_val) if not pd.isna(stock_val) else 0
        
        product = {
            "id": pid,
            "name": name,
            "stock": stock
        }
        latest_products.append(product)
        latest_products_by_id[pid.upper()] = product
        
    return latest_products, latest_products_by_id

# View all products
@router.get("/products")
def get_products():
    products, _ = load_latest_products()
    return products

# Check stock
@router.get("/stock/{product_id}")
def check_stock(product_id: str):
    search_id = product_id.strip().upper()
    
    # Normalize ID: if input is numeric like "005", convert to "P005"
    if not search_id.startswith("P") and search_id.isdigit():
        search_id = f"P{search_id}"
        
    _, products_by_id = load_latest_products()
    product = products_by_id.get(search_id)
    if product:
        return product

    return {"message": "Product not found"}




#   CSV File / Database                      
#         │
#         ▼
# load_latest_products()
#         │
#         ▼
# Convert DataFrame → Product List
#         │
#  ┌──────┴───────┐
#  ▼              ▼
# /products    /stock/{id}
# (View All)   (Check Stock)
#         │
#         ▼
#      User




#     Stock Quantity from CSV
#           │
#           ▼
#      Is it NaN?
#           │
#      ┌────┴────┐
#      │         │
#     No        Yes
#      │         │
#      ▼         ▼
#  int(value)    0
#      │         │
#      └────┬────┘
#           ▼
#       stock