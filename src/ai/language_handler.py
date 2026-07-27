from typing import Dict


class LanguageHandler:
    """
    Language detection and response language management
    """


    SUPPORTED_LANGUAGES = {

        "english": {
            "code": "en",
            "name": "English"
        },

        "tamil": {
            "code": "ta",
            "name": "Tamil"
        },

        "hindi": {
            "code": "hi",
            "name": "Hindi"
        },

        "urdu": {
            "code": "ur",
            "name": "Urdu"
        }
    }


    @staticmethod
    def detect_language(text: str) -> Dict:

        text = text.lower()


        # Tamil Unicode range
        if any(
            "\u0B80" <= char <= "\u0BFF"
            for char in text
        ):
            return {
                "language": "tamil",
                "code": "ta"
            }


        # Urdu / Arabic Unicode range
        if any(
            "\u0600" <= char <= "\u06FF"
            for char in text
        ):
            return {
                "language": "urdu",
                "code": "ur"
            }


        # Simple Hindi detection
        if any(
            "\u0900" <= char <= "\u097F"
            for char in text
        ):
            return {
                "language": "hindi",
                "code": "hi"
            }


        # Default
        return {
            "language": "english",
            "code": "en"
        }



    @staticmethod
    def get_response_prompt(language: str):

        prompts = {


            "english":
            """
            Reply in simple professional English.
            Be friendly and concise.
            """,


            "tamil":
            """
            Reply in natural Tamil.
            Use simple words that customers understand.
            """,


            "hindi":
            """
            Reply in simple Hindi.
            Maintain polite customer service tone.
            """,


            "urdu":
            """
            Reply in simple Urdu.
            Maintain respectful customer communication.
            """
        }


        return prompts.get(
            language,
            prompts["english"]
        )



    @staticmethod
    def is_supported(language: str):

        return (
            language
            in LanguageHandler.SUPPORTED_LANGUAGES
        )