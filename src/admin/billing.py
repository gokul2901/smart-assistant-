from datetime import datetime
from typing import List, Dict


class Billing:

    GST_PERCENTAGE = 18

    @staticmethod
    def calculate_subtotal(items: List[Dict]) -> float:
        """
        items = [
            {
                "product_name": "Rice",
                "quantity": 2,
                "price": 60
            }
        ]
        """

        subtotal = 0

        for item in items:
            subtotal += (
                item["quantity"] *
                item["price"]
            )

        return round(subtotal, 2)

    @staticmethod
    def calculate_gst(subtotal: float) -> float:

        gst_amount = (
            subtotal *
            Billing.GST_PERCENTAGE
        ) / 100

        return round(gst_amount, 2)

    @staticmethod
    def calculate_total(subtotal: float) -> float:

        gst_amount = Billing.calculate_gst(
            subtotal
        )

        total = subtotal + gst_amount

        return round(total, 2)

    @staticmethod
    def generate_invoice(
        order_id: str,
        customer_name: str,
        customer_phone: str,
        items: List[Dict]
    ):

        subtotal = Billing.calculate_subtotal(
            items
        )

        gst_amount = Billing.calculate_gst(
            subtotal
        )

        total = Billing.calculate_total(
            subtotal
        )

        invoice = {
            "invoice_id":
                f"INV-{order_id}",

            "order_id":
                order_id,

            "customer_name":
                customer_name,

            "customer_phone":
                customer_phone,

            "invoice_date":
                datetime.utcnow(),

            "items":
                items,

            "subtotal":
                subtotal,

            "gst_percentage":
                Billing.GST_PERCENTAGE,

            "gst_amount":
                gst_amount,

            "total_amount":
                total
        }

        return invoice