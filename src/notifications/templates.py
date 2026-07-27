from datetime import datetime


class NotificationTemplates:


    @staticmethod
    def order_confirmation(
        customer_name,
        order_id,
        amount
    ):

        return f"""
Hello {customer_name},

Your order has been confirmed.

Order ID: {order_id}
Total Amount: RS {amount}

Thank you for shopping with Gokul Departmental Store.

Date: {datetime.now().strftime('%d-%m-%Y')}
"""


    @staticmethod
    def order_status_update(
        order_id,
        status
    ):

        return f"""
Your order update:

Order ID: {order_id}

Current Status:
{status}

Thank you.
"""


    @staticmethod
    def delivery_message(
        order_id
    ):

        return f"""
Your order {order_id} is out for delivery.

Please keep your phone available.
"""


    @staticmethod
    def low_stock_alert(
        product_name,
        stock
    ):

        return f"""
Low Stock Alert!

Product:
{product_name}

Available Stock:
{stock}

Please update inventory.
"""