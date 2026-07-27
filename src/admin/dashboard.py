from src.admin.analytics import Analytics


class AdminDashboard:

    @staticmethod
    async def get_dashboard_data():

        analytics_data = (
            await Analytics.get_dashboard_summary()
        )

        low_stock = (
            await Analytics.get_low_stock_products()
        )

        top_products = (
            await Analytics.get_top_selling_products()
        )

        dashboard = {

            "summary": {
                "total_orders":
                    analytics_data["total_orders"],

                "total_customers":
                    analytics_data["total_customers"],

                "total_products":
                    analytics_data["total_products"],

                "total_revenue":
                    analytics_data["total_revenue"],

                "today_orders":
                    analytics_data["today_orders"],

                "today_revenue":
                    analytics_data["today_revenue"]
            },


            "inventory_alerts": {
                "low_stock_products":
                    low_stock
            },


            "sales_insights": {
                "top_selling_products":
                    top_products
            }

        }

        return dashboard