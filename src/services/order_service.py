from src.orders.order_manager import OrderManager



class OrderService:


    def __init__(self, database=None):

        self.order_manager = OrderManager(database)



    def create_customer_order(
        self,
        customer,
        items,
        amount,
        delivery_type,
        address=None
    ):


        return self.order_manager.create_order(

            customer_id=customer["id"],

            customer_name=customer["name"],

            phone_number=customer["phone"],

            items=items,

            total_amount=amount,

            delivery_type=delivery_type,

            address=address

        )