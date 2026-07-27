from src.orders.order_manager import OrderManager
from src.services.notification_service import NotificationService
from src.core.database import database

class OrderService:

    def __init__(self, db=None):
        self.db = db if db is not None else database
        self.order_manager = OrderManager(self.db)
        self.notification_service = NotificationService()

    def create_customer_order(
        self,
        customer,
        items,
        amount=None,
        delivery_type="Standard",
        address=None
    ):
        """Create order, generate GST invoice, save to Excel, and trigger simultaneous SMS + WhatsApp alerts."""
        cust_id = customer.get("id") or customer.get("customer_id") or "CUST-GUEST"
        cust_name = customer.get("name") or customer.get("customer_name") or "Valued Customer"
        phone = customer.get("phone") or customer.get("phone_number") or "9999999999"

        order = self.order_manager.create_order(
            customer_id=cust_id,
            customer_name=cust_name,
            phone_number=phone,
            items=items,
            total_amount=amount,
            delivery_type=delivery_type,
            address=address
        )

        # Trigger simultaneous SMS & WhatsApp alerts
        try:
            self.notification_service.send_dual_order_confirmation(
                phone=phone,
                name=cust_name,
                order_id=order["order_id"],
                amount=order["total_amount"],
                items=order["items"]
            )
        except Exception as err:
            print(f"Dual Notification Warning: {err}")

        return order

    async def create_order(self, order_model):
        """Handler for Pydantic Order model or dict from API."""
        if hasattr(order_model, "dict"):
            data = order_model.dict()
        else:
            data = dict(order_model)

        customer = {
            "id": data.get("customer_id", "CUST-GUEST"),
            "name": data.get("customer_name", "Customer"),
            "phone": data.get("phone_number", "9999999999")
        }

        return self.create_customer_order(
            customer=customer,
            items=data.get("items", []),
            amount=data.get("total_amount"),
            delivery_type=data.get("delivery_type", "Standard"),
            address=data.get("delivery_address") or data.get("address")
        )

    async def get_order_by_id(self, order_id):
        """Retrieve order from MongoDB Atlas."""
        if self.db is not None:
            order = await self.db.orders.find_one({"order_id": order_id}, {"_id": 0})
            if order:
                return order
        return None