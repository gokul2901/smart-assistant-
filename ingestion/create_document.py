from ingestion.csv_loader import df

documents = []

for _, row in df.iterrows():
    doc = f"""
    Product: {row['Name']}
    Category: {row['Category']}
    Brand: {row['Brand']}
    Price: {row['Price/RS']}
    Expiry Date: {row['Expiry Date']}
    Stock: {row['Stock Quantity']}
    Supplier: {row['Supplier']}
    Location: Block {row['Block Name']}, Rack {row['Rack No']}, Section {row['Session']}
    """.strip()
    documents.append(doc)

if __name__ == "__main__":
    print(documents[:2])



#csv_loader.py
#      ↓
#Read products.csv
#      ↓
#Store in DataFrame (df)
#      ↓
#Import here