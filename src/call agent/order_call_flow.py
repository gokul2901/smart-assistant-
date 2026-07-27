


from src.ai.intent_classifier import IntentClassifier
from src.ai.response_generator import ResponseGenerator



class OrderCallFlow:


    def __init__(self):

        self.response = ResponseGenerator()



    async def process(
        self,
        text
    ):


        intent = (
            IntentClassifier
            .classify(text)
        )


        if intent["intent"] == "create_order":


            return {

                "action":
                "create_order",

                "message":
                "Please tell product name and quantity"

            }



        result = await self.response.generate(

            user_query=text,

            context="",

            intent=intent["intent"]

        )


        return result