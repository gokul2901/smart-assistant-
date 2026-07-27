from langdetect import detect


class LanguageDetector:


    def detect(self, text):

        try:
            language = detect(text)

            return language

        except Exception:

            return "en"