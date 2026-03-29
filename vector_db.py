import os
import weaviate
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

class VectorDBManager:
    """
    Manager for Weaviate and Qdrant connections.
    """
    def __init__(self):
        # Weaviate connection (Multi-modal)
        self.weaviate_client = weaviate.Client(
            url=os.getenv("WEAVIATE_URL", "http://localhost:8080"),
            additional_headers={
                "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY", "") # for clip module if needed
            }
        )
        
        # Qdrant connection (Semantic RAG)
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333")
        )

    def initialize_schemas(self):
        """
        Ensures the schemas exist in both databases.
        """
        # Weaviate schema (Unstructured docs/images with clip)
        if not self.weaviate_client.schema.exists("UnstructuredDocument"):
            schema = {
                "class": "UnstructuredDocument",
                "vectorizer": "multi2vec-clip",
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                    {"name": "source", "dataType": ["string"]},
                    {"name": "original_id", "dataType": ["string"]}, # Shared UUID
                    {"name": "metadata", "dataType": ["text"]}
                ]
            }
            self.weaviate_client.schema.create_class(schema)
            
        # Qdrant collection (Tax Rules RAG)
        self.qdrant_client.recreate_collection(
            collection_name="statutory_rules",
            vectors_config={"size": 384, "distance": "Cosine"} # Matches all-MiniLM-L6-v2
        )

vector_db = VectorDBManager()
