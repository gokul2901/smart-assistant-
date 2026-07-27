from langdetect import detect



class LanguageDetector:


    def detect_language(
        self,
        text:str
    ):

        try:

            language = detect(text)

            return language


        except Exception:

            return "en"