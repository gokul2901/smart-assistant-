from notifications.templates import NotificationTemplates



class SMSService:


    def __init__(self):

        self.provider = "sms"



    def send_sms(
        self,
        phone_number,
        message
    ):

        """
        Send SMS message
        """

        print(
            f"Sending SMS to {phone_number}"
        )

        print(message)


        return {
            "status": "sent",
            "channel": "sms",
            "phone": phone_number
        }



    def send_order_sms(
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


        return self.send_sms(
            phone_number,
            message
        )