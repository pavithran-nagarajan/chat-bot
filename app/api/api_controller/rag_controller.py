from fastapi import APIRouter, UploadFile, File
from app.api.api_business.rag_business import add_documents
from app.business.common_business.document_loader_business import extract_text
from app.business.common_business.logging_business import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text(content, file.filename)
    add_documents([text])
    return {"message": f"{file.filename} uploaded successfully!"}

@router.post("/upload-text")
async def upload_text(text: str):
    add_documents([text])
    return {"message": "Text added successfully!"}