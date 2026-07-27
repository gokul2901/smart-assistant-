# src/admin/reports.py

from datetime import datetime, timedelta
from src.core.database import db


class Reports:

    """
    Admin business reports
    - Sales reports
    - Product reports
    - Inventory reports
    - Customer reports
    """

    @staticmethod
    async def daily_sales_report():

        start = datetime.utcnow().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        pipeline = [
            {
                "$match": {
                    "created_at": {
                        "$gte": start
                    },
                    "status": "completed"
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_orders": {
                        "$sum": 1
                    },
                    "total_sales": {
                        "$sum": "$total_amount"
                    }
                }
            }
        ]

        result = await db.orders.aggregate(
            pipeline
        ).to_list(1)

        return result[0] if result else {
            "total_orders": 0,
            "total_sales": 0
        }


    @staticmethod
    async def monthly_sales_report():

        start = datetime.utcnow().replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        pipeline = [
            {
                "$match": {
                    "created_at": {
                        "$gte": start
                    },
                    "status": "completed"
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dayOfMonth": "$created_at"
                    },
                    "orders": {
                        "$sum": 1
                    },
                    "sales": {
                        "$sum": "$total_amount"
                    }
                }
            },
            {
                "$sort": {
                    "_id": 1
                }
            }
        ]

        return await db.orders.aggregate(
            pipeline
        ).to_list(None)


    @staticmethod
    async def top_products(limit: int = 10):

        pipeline = [
            {
                "$unwind": "$items"
            },
            {
                "$group": {
                    "_id": "$items.product_name",
                    "quantity_sold": {
                        "$sum": "$items.quantity"
                    },
                    "revenue": {
                        "$sum": {
                            "$multiply": [
                                "$items.quantity",
                                "$items.price"
                            ]
                        }
                    }
                }
            },
            {
                "$sort": {
                    "quantity_sold": -1
                }
            },
            {
                "$limit": limit
            }
        ]

        return await db.orders.aggregate(
            pipeline
        ).to_list(limit)


    @staticmethod
    async def inventory_report():

        products = await db.products.find(
            {},
            {
                "_id": 0,
                "product_name": 1,
                "category": 1,
                "stock": 1,
                "price": 1
            }
        ).to_list(1000)

        return products


    @staticmethod
    async def low_stock_report(
        threshold: int = 10
    ):

        products = await db.products.find(
            {
                "stock": {
                    "$lte": threshold
                }
            },
            {
                "_id": 0,
                "product_name": 1,
                "stock": 1
            }
        ).to_list(100)

        return products


    @staticmethod
    async def customer_purchase_report(
        limit: int = 20
    ):

        pipeline = [
            {
                "$group": {
                    "_id": "$customer_id",
                    "orders": {
                        "$sum": 1
                    },
                    "spent": {
                        "$sum": "$total_amount"
                    }
                }
            },
            {
                "$sort": {
                    "spent": -1
                }
            },
            {
                "$limit": limit
            }
        ]

        return await db.orders.aggregate(
            pipeline
        ).to_list(limit)