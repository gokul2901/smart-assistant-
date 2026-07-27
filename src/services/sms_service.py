from src.notifications.sms import SMSService



class SMSNotificationService:


    def __init__(self):

        self.client = SMSService()



    def send_sms(
        self,
        phone,
        message
    ):


        return self.client.send_sms(

            phone,

            message

        )