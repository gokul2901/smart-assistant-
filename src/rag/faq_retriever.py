class FAQRetriever:


    def __init__(self):

        self.faq_data = [

            {
                "question":
                "What is shop opening time?",

                "answer":
                "Our shop is open from 9 AM to 9 PM."
            },


            {
                "question":
                "Do you provide home delivery?",

                "answer":
                "Yes, home delivery is available."
            },


            {
                "question":
                "What payment methods are available?",

                "answer":
                "We accept cash, UPI and cards."
            }

        ]



    def search(
        self,
        query:str
    ):

        query = query.lower()


        results=[]


        for faq in self.faq_data:

            if any(
                word in faq["question"].lower()
                for word in query.split()
            ):

                results.append(
                    faq
                )


        return results