from typing import List

from ibm_watsonx_ai.foundation_models import Embeddings


# Need to define an Embedding Function for the documents
class watsonxEmbeddingFunction:
    """An embedding function to enable the embeddings against the passed in embedding_model"""

    def __init__(self, embedding_model: Embeddings):
        """Creates a watsonxEmbeddingFunction

        Args:
            embedding_model (Embeddings): The Embedding model to use
        """
        self.__the_model = embedding_model

    def embed_documents(self, document_list: List[str]) -> List[List[float]]:
        return self.__the_model.embed_documents(document_list)

    def embed_query(self, query) -> List[float]:
        return self.__the_model.embed_query(query)
