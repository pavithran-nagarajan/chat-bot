import os
from app.business.enum_business.enum import VectorDBType

def get_vector_db_type() -> VectorDBType:
    str_vector_db = os.getenv("VECTOR_DB", VectorDBType.CHROMA.value)
    try:
        return VectorDBType(str_vector_db)
    except ValueError:
        raise ValueError(f"Unsupported VECTOR_DB: '{str_vector_db}'. Choose from: {[e.value for e in VectorDBType]}")
