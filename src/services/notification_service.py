from src.services.whatsapp_service import (
    WhatsAppNotificationService
)

from src.services.sms_service import (
    SMSNotificationService
)



class NotificationService:


    def __init__(self):

        self.whatsapp = (
            WhatsAppNotificationService()
        )

        self.sms = (
            SMSNotificationService()
        )



    def send_order_alert(
        self,
        phone,
        name,
        order_id,
        amount
    ):


        whatsapp_response = (
            self.whatsapp
            .send_order_confirmation(
                phone,
                name,
                order_id,
                amount
            )
        )


        return whatsapp_response