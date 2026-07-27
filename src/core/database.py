# src/core/database.py

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL") or os.getenv("MANGODB_API_URL")
if not MONGO_URL:
    raise ValueError("MONGO_URL or MANGODB_API_URL is not set in environment variables.")



client = AsyncIOMotorClient(
    MONGO_URL
)


database = client[
    "department_store"
]

db = database



# Collections

products_collection = database.products

orders_collection = database.orders

users_collection = database.users

inventory_collection = database.inventory


async def check_database():

    try:

        await client.admin.command(
            "ping"
        )

        return True

    except Exception:

        return False