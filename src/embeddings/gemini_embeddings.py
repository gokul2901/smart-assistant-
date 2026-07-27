import google.generativeai as genai

from config.settings import settings


class GeminiEmbedding:

    def __init__(self):

        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.EMBEDDING_MODEL


    def generate_embedding(self, text: str):

        """
        Generate single text embedding
        """

        response = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_document"
        )

        return response["embedding"]



    def generate_embeddings(self, texts:list):

        """
        Generate multiple embeddings
        """

        embeddings = []

        for text in texts:

            embedding = self.generate_embedding(text)

            embeddings.append(embedding)


        return embeddings