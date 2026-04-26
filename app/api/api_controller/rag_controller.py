from fastapi import APIRouter, UploadFile, File
from app.api.api_business.rag_business import add_documents

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    add_documents([text])
    return {"message": f"{file.filename} uploaded successfully!"}

@router.post("/upload-text")
async def upload_text(text: str):
    add_documents([text])
    return {"message": "Text added successfully!"}