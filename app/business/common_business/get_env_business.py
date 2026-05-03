import os
from dotenv import load_dotenv
from app.business.enum_business.enum import VectorDBType

load_dotenv()

def get_env(key: str, default: str = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable '{key}' is not set and has no default.")
    return value

def get_vector_db_type() -> VectorDBType:
    str_vector_db = os.getenv("VECTOR_DB", VectorDBType.CHROMA.value)
    try:
        return VectorDBType(str_vector_db)
    except ValueError:
        raise ValueError(f"Unsupported VECTOR_DB: '{str_vector_db}'. Choose from: {[e.value for e in VectorDBType]}")
    

