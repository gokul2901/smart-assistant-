from datetime import datetime, timedelta

from src.core.database import db


class Analytics:
    """
    Business analytics service

    Provides:
    - Sales summary
    - Order statistics
    - Product statistics
    - Inventory statistics
    """


    @staticmethod
    async def get_dashboard_summary():
        """
        Main admin dashboard analytics
        """

        today = datetime.utcnow().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )


        # Today's sales

        sales_pipeline = [

            {
                "$match": {
                    "created_at": {
                        "$gte": today
                    },
                    "status": "completed"
                }
            },

            {
                "$group": {

                    "_id": None,

                    "total_sales": {
                        "$sum": "$total_amount"
                    },

                    "total_orders": {
                        "$sum": 1
                    }

                }
            }

        ]


        sales_result = await db.orders.aggregate(
            sales_pipeline
        ).to_list(1)



        sales_data = (
            sales_result[0]
            if sales_result
            else {
                "total_sales": 0,
                "total_orders": 0
            }
        )



        # Total products

        total_products = await db.products.count_documents(
            {}
        )



        # Low stock products

        low_stock = await db.products.count_documents(
            {
                "stock": {
                    "$lte": 10
                }
            }
        )



        # Total customers

        total_customers = await db.users.count_documents(
            {}
        )



        return {

            "today_sales":
                sales_data["total_sales"],

            "today_orders":
                sales_data["total_orders"],

            "total_products":
                total_products,

            "low_stock_products":
                low_stock,

            "total_customers":
                total_customers

        }



    @staticmethod
    async def monthly_sales():

        start_date = datetime.utcnow().replace(
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
                        "$gte": start_date
                    },

                    "status": "completed"

                }
            },


            {
                "$group": {

                    "_id": None,

                    "sales": {
                        "$sum": "$total_amount"
                    },

                    "orders": {
                        "$sum": 1
                    }

                }
            }

        ]


        result = await db.orders.aggregate(
            pipeline
        ).to_list(1)


        return (
            result[0]
            if result
            else {
                "sales": 0,
                "orders": 0
            }
        )



    @staticmethod
    async def top_selling_products(
        limit: int = 10
    ):

        pipeline = [

            {
                "$unwind": "$items"
            },


            {
                "$group": {

                    "_id":
                    "$items.product_name",

                    "quantity":
                    {
                        "$sum":
                        "$items.quantity"
                    }

                }
            },


            {
                "$sort":
                {
                    "quantity": -1
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
    async def inventory_summary():

        total = await db.products.count_documents(
            {}
        )


        available = await db.products.count_documents(
            {
                "stock": {
                    "$gt": 0
                }
            }
        )


        out_of_stock = await db.products.count_documents(
            {
                "stock": 0
            }
        )


        return {

            "total_products": total,

            "available_products": available,

            "out_of_stock_products":
                out_of_stock

        }