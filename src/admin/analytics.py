from datetime import datetime, timedelta
from src.core.database import db


class Analytics:

    @staticmethod
    async def get_total_orders():
        return await db.orders.count_documents({})

    @staticmethod
    async def get_total_customers():
        return await db.customers.count_documents({})

    @staticmethod
    async def get_total_products():
        return await db.products.count_documents({})

    @staticmethod
    async def get_total_revenue():
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_revenue": {
                        "$sum": "$total_amount"
                    }
                }
            }
        ]

        result = await db.orders.aggregate(pipeline).to_list(1)

        if result:
            return result[0]["total_revenue"]

        return 0

    @staticmethod
    async def get_today_orders():
        today = datetime.utcnow().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        return await db.orders.count_documents(
            {
                "created_at": {
                    "$gte": today
                }
            }
        )

    @staticmethod
    async def get_today_revenue():

        today = datetime.utcnow().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        pipeline = [
            {
                "$match": {
                    "created_at": {
                        "$gte": today
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "revenue": {
                        "$sum": "$total_amount"
                    }
                }
            }
        ]

        result = await db.orders.aggregate(
            pipeline
        ).to_list(1)

        if result:
            return result[0]["revenue"]

        return 0

    @staticmethod
    async def get_low_stock_products(
        threshold=10
    ):

        products = await db.products.find(
            {
                "stock": {
                    "$lte": threshold
                }
            }
        ).to_list(length=100)

        return products

    @staticmethod
    async def get_top_selling_products(
        limit=5
    ):

        pipeline = [
            {
                "$group": {
                    "_id": "$product_name",
                    "total_sold": {
                        "$sum": "$quantity"
                    }
                }
            },
            {
                "$sort": {
                    "total_sold": -1
                }
            },
            {
                "$limit": limit
            }
        ]

        return await db.order_items.aggregate(
            pipeline
        ).to_list(limit)

    @staticmethod
    async def get_dashboard_summary():

        return {
            "total_orders":
                await Analytics.get_total_orders(),

            "total_customers":
                await Analytics.get_total_customers(),

            "total_products":
                await Analytics.get_total_products(),

            "total_revenue":
                await Analytics.get_total_revenue(),

            "today_orders":
                await Analytics.get_today_orders(),

            "today_revenue":
                await Analytics.get_today_revenue()
        }