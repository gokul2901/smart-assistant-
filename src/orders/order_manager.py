import os
import uuid
from datetime import datetime
import pandas as pd

from src.orders.order_status import OrderStatus
from src.admin.billing import Billing

class OrderManager:

    def __init__(self, database=None):
        self.database = database
        self.export_excel_path = "data/exports/orders.xlsx"
        self.export_csv_path = "data/exports/orders.csv"

    def _export_to_excel(self, order, invoice):
        """Automatically append order record to Excel & CSV sheet."""
        exports_dir = "data/exports"
        if os.path.isfile(exports_dir):
            os.remove(exports_dir)
        os.makedirs(exports_dir, exist_ok=True)

        items_str = ", ".join([
            f"{it.get('product_name', it.get('name', 'Product'))} (x{it.get('quantity', 1)})"
            for it in order.get("items", [])
        ])

        new_row = {
            "Order ID": order["order_id"],
            "Date": order["created_at"].strftime("%Y-%m-%d %H:%M:%S"),
            "Customer ID": order.get("customer_id", "N/A"),
            "Customer Name": order.get("customer_name", "Customer"),
            "Phone Number": order.get("phone_number", "N/A"),
            "Items Purchased": items_str,
            "Subtotal (RS)": invoice.get("subtotal", 0.0),
            "GST 18% (RS)": invoice.get("gst_amount", 0.0),
            "Total Amount (RS)": invoice.get("total_amount", order.get("total_amount", 0.0)),
            "Delivery Type": order.get("delivery_type", "Standard"),
            "Delivery Address": order.get("delivery_address", "Store Pickup"),
            "Status": order.get("status", OrderStatus.CREATED)
        }

        new_df = pd.DataFrame([new_row])

        # Append to Excel
        if os.path.exists(self.export_excel_path):
            try:
                existing_df = pd.read_excel(self.export_excel_path)
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            except Exception:
                combined_df = new_df
        else:
            combined_df = new_df

        combined_df.to_excel(self.export_excel_path, index=False)

        # Append to CSV
        if os.path.exists(self.export_csv_path):
            new_df.to_csv(self.export_csv_path, mode='a', header=False, index=False)
        else:
            new_df.to_csv(self.export_csv_path, index=False)

    def create_order(
        self,
        customer_id,
        customer_name,
        phone_number,
        items,
        total_amount=None,
        delivery_type="Standard",
        address=None
    ):
        """Create new customer order with billing invoice, Excel export, and MongoDB record."""
        order_id = "ORD-" + str(uuid.uuid4())[:8].upper()

        formatted_items = []
        for it in items:
            pname = it.get("product_name") or it.get("name") or "Item"
            qty = it.get("quantity", 1)
            price = it.get("price", 0.0)
            formatted_items.append({
                "product_name": pname,
                "quantity": qty,
                "price": price
            })

        # 1. Generate Billing Session Invoice
        invoice = Billing.generate_invoice(
            order_id=order_id,
            customer_name=customer_name,
            customer_phone=phone_number,
            items=formatted_items
        )

        final_total = invoice["total_amount"] if invoice["total_amount"] > 0 else (total_amount or 0.0)

        order = {
            "order_id": order_id,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "phone_number": phone_number,
            "items": formatted_items,
            "subtotal": invoice["subtotal"],
            "gst_amount": invoice["gst_amount"],
            "total_amount": final_total,
            "delivery_type": delivery_type,
            "delivery_address": address or "Store Pickup",
            "status": OrderStatus.CREATED,
            "invoice": invoice,
            "created_at": datetime.now()
        }

        # 2. Persist to MongoDB Atlas
        if self.database is not None:
            try:
                if hasattr(self.database.orders, "insert_one"):
                    self.database.orders.insert_one(order)
                    self.database.invoices.insert_one(invoice)
            except Exception as err:
                print(f"MongoDB Insert Warning: {err}")

        # 3. Export to Excel & CSV Sheet
        try:
            self._export_to_excel(order, invoice)
        except Exception as err:
            print(f"Excel Export Warning: {err}")

        return order

    def update_order_status(self, order_id, status):
        """Update order status in MongoDB."""
        if self.database is not None:
            try:
                self.database.orders.update_one(
                    {"order_id": order_id},
                    {"$set": {"status": status, "updated_at": datetime.now()}}
                )
            except Exception as err:
                print(f"MongoDB Update Warning: {err}")

        return {
            "order_id": order_id,
            "new_status": status
        }