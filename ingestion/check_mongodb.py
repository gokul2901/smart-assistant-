import os
from dotenv import load_dotenv
from pymongo import MongoClient

env_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path=env_path)

MONGO_URL = os.getenv("MONGO_URL") or os.getenv("MANGODB_API_URL")

def check_mongodb_insights():
    client = MongoClient(MONGO_URL)
    db = client["department_store"]
    collection = db["products"]

    total_count = collection.count_documents({})
    categories = collection.distinct("category")

    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "count": {"$sum": 1},
                "avg_price": {"$avg": "$price"},
                "total_stock": {"$sum": "$stock"}
            }
        },
        {"$sort": {"count": -1}}
    ]

    stats = list(collection.aggregate(pipeline))

    print("==================================================")
    print("           MONGODB ATLAS INSIGHTS REPORT          ")
    print("==================================================")
    print(f"Database Name       : department_store")
    print(f"Collection Name     : products")
    print(f"Total Products      : {total_count}")
    print(f"Total Categories    : {len(categories)}")
    print("--------------------------------------------------")
    print(f"{'Category':<25} | {'Count':<6} | {'Avg Price (RS)':<14} | {'Total Stock':<10}")
    print("--------------------------------------------------")
    for s in stats[:10]:
        cat = str(s['_id'])[:24]
        cnt = s['count']
        price = round(s.get('avg_price', 0), 2)
        stock = s.get('total_stock', 0)
        print(f"{cat:<25} | {cnt:<6} | {price:<14} | {stock:<10}")

    print("--------------------------------------------------")
    print("Sample Product Document:")
    sample = collection.find_one({}, {"_id": 0})
    if sample:
        for k, v in sample.items():
            print(f"  {k}: {v}")
    print("==================================================")
    client.close()

if __name__ == "__main__":
    check_mongodb_insights()
