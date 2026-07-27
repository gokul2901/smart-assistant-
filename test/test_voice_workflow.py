import unittest
import os
import sys
sys.path.insert(0, os.getcwd())

import pandas as pd
from src.orders.order_manager import OrderManager
from src.services.order_service import OrderService
from src.services.notification_service import NotificationService

class TestVoiceOrderWorkflow(unittest.TestCase):

    def setUp(self):
        self.order_service = OrderService()

    def test_order_creation_excel_and_dual_notifications(self):
        customer = {
            "id": "CUST-TEST-001",
            "name": "Arun Kumar",
            "phone": "9876543210"
        }
        items = [
            {"product_name": "Aashirvaad Atta", "quantity": 2, "price": 280.0},
            {"product_name": "Okra", "quantity": 1, "price": 50.0}
        ]

        order = self.order_service.create_customer_order(
            customer=customer,
            items=items,
            delivery_type="Express Delivery",
            address="123 Main Street, Bangalore"
        )

        # 1. Verify Order ID format
        self.assertTrue(order["order_id"].startswith("ORD-"))

        # 2. Verify GST Invoice Calculation (18%)
        expected_subtotal = (2 * 280.0) + (1 * 50.0)  # 610.0
        expected_gst = round(expected_subtotal * 0.18, 2)  # 109.8
        expected_total = expected_subtotal + expected_gst  # 719.8

        self.assertEqual(order["subtotal"], expected_subtotal)
        self.assertEqual(order["gst_amount"], expected_gst)
        self.assertEqual(order["total_amount"], expected_total)

        # 3. Verify Excel Export
        excel_path = "data/exports/orders.xlsx"
        self.assertTrue(os.path.exists(excel_path))

        df = pd.read_excel(excel_path)
        self.assertGreater(len(df), 0)
        self.assertIn(order["order_id"], df["Order ID"].values)

    def test_dual_notification_service(self):
        notif_service = NotificationService()
        result = notif_service.send_dual_order_confirmation(
            phone="9876543210",
            name="Arun Kumar",
            order_id="ORD-TEST1234",
            amount=719.80
        )
        self.assertEqual(result["order_id"], "ORD-TEST1234")
        self.assertEqual(result["whatsapp_status"], "sent")
        self.assertEqual(result["sms_status"], "sent")

if __name__ == "__main__":
    unittest.main()
