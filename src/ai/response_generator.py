from src.ai.llm_router import LLMRouter
from src.ai.language_handler import LanguageHandler
from loguru import logger


class ResponseGenerator:
    """
    Generate final customer response
    using RAG context + LLM
    """


    def __init__(self):

        self.llm = LLMRouter()


    async def generate(
        self,
        user_query: str,
        context: str = "",
        intent: str = "general_chat"
    ):

        try:

            # Detect customer language
            language_info = (
                LanguageHandler
                .detect_language(user_query)
            )

            language = (
                language_info["language"]
            )


            # Language instruction
            language_prompt = (
                LanguageHandler
                .get_response_prompt(language)
            )


            system_prompt = f"""
You are a helpful departmental store voice assistant.

Rules:
- Answer only from provided context.
- Do not create fake product information.
- Be polite and short.
- Help customers with products, stock, offers and orders.

Customer intent:
{intent}

Response language:
{language}

{language_prompt}


Store Knowledge:
{context}
"""


            messages = [

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_query
                }

            ]


            # Generate response using LLM fallback
            result = await self.llm.generate_response(
                messages
            )


            return {

                "response":
                    result["response"],

                "language":
                    language,

                "model":
                    result["model"],

                "intent":
                    intent
            }


        except Exception as error:

            logger.error(
                f"Response generation failed: {error}"
            )


            return {

                "response":
                    "Sorry, I could not process your request.",

                "language":
                    "english",

                "model":
                    "none",

                "intent":
                    intent
            }