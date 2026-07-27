from src.embeddings.gemini_embeddings import GeminiEmbedding



class EmbeddingFactory:


    @staticmethod
    def get_embedding_model(provider="gemini"):


        if provider == "gemini":

            return GeminiEmbedding()


        else:

            raise ValueError(
                "Unsupported embedding provider"
            )