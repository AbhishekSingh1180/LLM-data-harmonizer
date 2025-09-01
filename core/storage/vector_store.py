import uuid
import chromadb
from typing import Union, Any
from sentence_transformers import SentenceTransformer
import logging
import urllib3

# Suppress warnings from urllib3 used by chromadb
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("backoff").disabled = True
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VectorStoreClient:
    def __init__(self, collection_name, model_name="all-MiniLM-L6-v2",
                 persist_directory="./core/storage/chroma_db/"):
        self.chroma_client = chromadb.PersistentClient(persist_directory)
        self.model = SentenceTransformer(model_name)
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

    def store_embeddings(self, query: Any,
                         query_to_text_fn: Union[callable, None] = None):

        if query_to_text_fn is None:
            query_to_text_fn = lambda x: str(x)
        query_text = query_to_text_fn(query)
        embedding = self.model.encode([query_text])[0]
        metadata = {
            "domain": query.get("domain", ""),
            "description": query.get("description", "")
        }
        self.collection.add(
            ids=[str(uuid.uuid4())],
            documents=[query_text],
            embeddings=[embedding],
            metadatas=[metadata]
        )

    def query(self, query: Any,
              n_results=1,
              query_to_text_fn: Union[callable, None] = None) -> dict:

        if query_to_text_fn is None:
            query_to_text_fn = lambda x: str(x)
        query_text = query_to_text_fn(query)
        embedding = self.model.encode([query_text])[0]
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
