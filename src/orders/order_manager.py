from datetime import datetime
import uuid

from src.orders.order_status import OrderStatus



class OrderManager:


    def __init__(self, database=None):

        self.database = database


    def create_order(
        self,
        customer_id,
        customer_name,
        phone_number,
        items,
        total_amount,
        delivery_type,
        address=None
    ):

        """
        Create new customer order
        """


        order_id = (
            "ORD-" +
            str(uuid.uuid4())[:8].upper()
        )


        order = {

            "order_id": order_id,

            "customer_id": customer_id,

            "customer_name": customer_name,

            "phone_number": phone_number,

            "items": items,

            "total_amount": total_amount,

            "delivery_type": delivery_type,

            "delivery_address": address,

            "status": OrderStatus.CREATED,

            "created_at": datetime.utcnow()

        }


        # MongoDB insert
        if self.database:

            self.database.orders.insert_one(
                order
            )


        return order



    def update_order_status(
        self,
        order_id,
        status
    ):

        """
        Update order status
        """


        if self.database:

            self.database.orders.update_one(

                {
                    "order_id": order_id
                },

                {
                    "$set":
                    {
                        "status": status,
                        "updated_at": datetime.utcnow()
                    }
                }

            )


        return {

            "order_id": order_id,

            "new_status": status

        }