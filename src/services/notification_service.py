from src.services.whatsapp_service import WhatsAppNotificationService
from src.services.sms_service import SMSNotificationService

class NotificationService:

    def __init__(self):
        self.whatsapp = WhatsAppNotificationService()
        self.sms = SMSNotificationService()

    def send_order_alert(
        self,
        phone,
        name,
        order_id,
        amount
    ):
        whatsapp_res = self.whatsapp.send_order_confirmation(
            phone=phone, name=name, order_id=order_id, amount=amount
        )
        sms_res = self.sms.send_order_sms(
            phone=phone, customer_name=name, order_id=order_id, amount=amount
        )
        return {
            "whatsapp": whatsapp_res,
            "sms": sms_res
        }

    def send_dual_order_confirmation(
        self,
        phone,
        name,
        order_id,
        amount,
        items=None
    ):
        """Send WhatsApp and SMS notifications simultaneously upon order completion."""
        print(f"Simultaneously triggering SMS + WhatsApp order alert to {phone} for Order {order_id}")

        wa_result = self.whatsapp.send_order_confirmation(
            phone=phone,
            name=name,
            order_id=order_id,
            amount=amount
        )

        sms_result = self.sms.send_order_sms(
            phone=phone,
            customer_name=name,
            order_id=order_id,
            amount=amount
        )

        return {
            "order_id": order_id,
            "phone": phone,
            "whatsapp_status": wa_result.get("status"),
            "sms_status": sms_result.get("status")
        }