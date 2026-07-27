class LanguageManager:


    def __init__(self):

        self.supported = {

            "en": "English",
            "ta": "Tamil",
            "hi": "Hindi",
            "ur": "Urdu",
            "fr": "French",
            "de": "German",
            "es": "Spanish",
            "it": "Italian",
            "ja": "Japanese",
            "ko": "Korean",
            "zh": "Chinese",
            "ar": "Arabic"

        }



    def get_language_name(
        self,
        code
    ):

        return self.supported.get(
            code,
            "Auto Detect"
        ) 