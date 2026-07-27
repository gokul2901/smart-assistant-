from src.embeddings.gemini_embeddings import GeminiEmbedding


class MultilingualEmbedding:

    def __init__(self):
        self.embedding = GeminiEmbedding()


    def create_embedding(self, text, language):

        # Future language preprocessing

        if language == "tamil":
            text = self.translate_tamil(text)

        elif language == "hindi":
            text = self.translate_hindi(text)


        return self.embedding.generate_embedding(text)


    def translate_tamil(self, text):
        return text


    def translate_hindi(self, text):
        return text