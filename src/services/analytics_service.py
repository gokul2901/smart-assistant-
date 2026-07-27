class AnalyticsService:


    def __init__(self, database=None):

        self.database = database



    def total_orders(self):

        if self.database:

            return self.database.orders.count_documents({})


        return 0



    def total_sales(self):

        if self.database:

            pipeline = [

                {
                    "$group":
                    {
                        "_id": None,

                        "total":
                        {
                            "$sum":
                            "$total_amount"
                        }
                    }
                }

            ]


            result = list(
                self.database.orders.aggregate(
                    pipeline
                )
            )

            return result


        return 0