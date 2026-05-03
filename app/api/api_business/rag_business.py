from app.business.vector_db_business.chroma_business import chroma_add_documents, chroma_search_documents
from app.business.common_business.get_env_business import get_vector_db_type
from app.business.enum_business.enum import VectorDBType

def add_documents(texts: list[str]) -> None:
    vector_db = get_vector_db_type()
    if vector_db == VectorDBType.CHROMA:
        chroma_add_documents(texts)

def search_documents(query: str, k: int = 3) -> str:
    vector_db = get_vector_db_type()
    if vector_db == VectorDBType.CHROMA:
        return chroma_search_documents(query, k)
    return ""