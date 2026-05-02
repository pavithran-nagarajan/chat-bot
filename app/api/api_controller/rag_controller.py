from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.api.api_business.rag_business import add_documents
from app.business.common_business.document_loader_business import extract_text
from app.business.common_business.logging_business import get_logger
from app.business.common_business.logging_business import logging

router = APIRouter()
logger = get_logger(__name__)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    job_api_response = {}
    job_api_response["Message"] = "";
    try:
        content = await file.read()
        text = extract_text(content, file.filename)
        add_documents([text])
        job_api_response["Message"] = f"{file.filename} uploaded successfully!";
        return job_api_response
    except Exception as e:
        logging.critical(
            f"Unhandled exception | {str(e)}",
            exc_info=e
        )
        job_api_response["Message"] = "Internal server error"
        return JSONResponse(status_code=500, content=job_api_response)

@router.post("/upload-text")
async def upload_text(text: str):
    job_api_response = {}
    job_api_response["Message"] = "";
    try:
        add_documents([text])
        job_api_response["Message"] = "Text added successfully!";
        return job_api_response
    except Exception as e:
        logging.critical(
            f"Unhandled exception | {str(e)}",
            exc_info=e
        )
        job_api_response["Message"] = "Internal server error"
        return JSONResponse(status_code=500, content=job_api_response)