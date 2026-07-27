from langdetect import detect



class LanguageUtils:



    SUPPORTED_LANGUAGES = {

        "en": "English",

        "ta": "Tamil",

        "hi": "Hindi",

        "ur": "Urdu"

    }



    @staticmethod
    def detect_language(
        text:str
    ):

        """
        Detect customer language
        """

        try:

            language = detect(text)


            if language in (
                LanguageUtils
                .SUPPORTED_LANGUAGES
            ):

                return language


            return "en"


        except Exception:

            return "en"



    @staticmethod
    def normalize_text(
        text:str
    ):

        """
        Clean user input
        """

        text = text.strip()

        text = " ".join(
            text.split()
        )


        return text



    @staticmethod
    def get_language_name(
        code:str
    ):

        return (
            LanguageUtils
            .SUPPORTED_LANGUAGES
            .get(
                code,
                "English"
            )
        )