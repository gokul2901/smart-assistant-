class ContextBuilder:


    def build_context(
        self,
        query,
        retrieved_documents,
        chat_history=None
    ):


        context = {

            "user_query": query,

            "documents": retrieved_documents,

            "history": chat_history or []

        }


        return context



    def create_prompt_context(
        self,
        context
    ):


        documents = "\n".join(
            context["documents"]
        )


        prompt = f"""

Customer Question:
{context['user_query']}


Relevant Information:
{documents}


Conversation History:
{context['history']}

"""


        return prompt