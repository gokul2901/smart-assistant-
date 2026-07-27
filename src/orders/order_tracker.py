from datetime import datetime



class OrderTracker:


    def __init__(self, database=None):

        self.database = database



    def get_order_status(
        self,
        order_id
    ):

        """
        Get current order status
        """


        if self.database:

            order = (
                self.database.orders
                .find_one(
                    {
                        "order_id": order_id
                    }
                )
            )


            if order:

                return {

                    "order_id": order_id,

                    "status": order.get(
                        "status"
                    ),

                    "updated_at": order.get(
                        "updated_at"
                    )

                }


        return {

            "message":
            "Order not found"

        }



    def get_customer_orders(
        self,
        customer_id
    ):

        """
        Get customer order history
        """


        if self.database:

            orders = list(

                self.database.orders.find(
                    {
                        "customer_id":
                        customer_id
                    }
                )

            )

            return orders


        return []