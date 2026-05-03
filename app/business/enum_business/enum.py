from enum import Enum, IntEnum, auto

class VectorDBType(Enum):
    CHROMA = "chroma"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"
    QDRANT = "qdrant"
    FAISS = "faiss"
