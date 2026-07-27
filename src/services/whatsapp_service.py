from src.notifications.whatsapp import WhatsAppService



class WhatsAppNotificationService:


    def __init__(self):

        self.client = WhatsAppService()



    def send_order_confirmation(
        self,
        phone,
        name,
        order_id,
        amount
    ):


        return self.client.send_order_confirmation(

            phone,

            name,

            order_id,

            amount

        )