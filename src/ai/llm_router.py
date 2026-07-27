import os
from litellm import completion
from loguru import logger


class LLMRouter:
    """
    LLM fallback manager

    Priority:
    1. GLM
    2. Grok
    3. Mistral
    """

    def __init__(self):

        self.models = [

            {
                "name": "glm",
                "model": "glm/glm-4",
                "api_key": os.getenv(
                    "GLM_API_KEY"
                )
            },

            {
                "name": "grok",
                "model": "xai/grok-beta",
                "api_key": os.getenv(
                    "GROK_API_KEY"
                )
            },

            {
                "name": "mistral",
                "model": "mistral/mistral-large",
                "api_key": os.getenv(
                    "MISTRAL_API_KEY"
                )
            }
        ]


    async def generate_response(
        self,
        messages,
        temperature=0.3
    ):

        for llm in self.models:

            try:

                logger.info(
                    f"Trying LLM: {llm['name']}"
                )


                response = completion(

                    model=llm["model"],

                    messages=messages,

                    temperature=temperature,

                    api_key=llm["api_key"]

                )


                content = (
                    response
                    .choices[0]
                    .message.content
                )


                logger.info(
                    f"Success: {llm['name']}"
                )


                return {
                    "model":
                        llm["name"],

                    "response":
                        content
                }


            except Exception as error:

                logger.warning(
                    f"{llm['name']} failed: {error}"
                )


        return {
            "model": "none",
            "response":
                "Sorry, I am unable to process your request right now."
        }