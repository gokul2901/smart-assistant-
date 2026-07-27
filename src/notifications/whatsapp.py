from src.notifications.templates import NotificationTemplates



class WhatsAppService:


    def __init__(self):

        self.provider = "whatsapp"



    def send_message(
        self,
        phone_number,
        message
    ):

        """
        Send WhatsApp message
        """

        print(
            f"Sending WhatsApp message to {phone_number}"
        )

        print(message)


        return {
            "status": "sent",
            "channel": "whatsapp",
            "phone": phone_number
        }



    def send_order_confirmation(
        self,
        phone_number,
        customer_name,
        order_id,
        amount
    ):

        message = (
            NotificationTemplates
            .order_confirmation(
                customer_name,
                order_id,
                amount
            )
        )


        return self.send_message(
            phone_number,
            message
        )