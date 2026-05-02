from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.api.api_business.chat_business import generate_reply
from app.business.common_business.logging_business import logging

router = APIRouter()
sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    job_api_response = {}
    job_api_response["Message"] = "";
    try:
        history = sessions.setdefault(req.session_id, [
            {"role": "system", "content": "You are a helpful assistant."}
        ])
        history.append({"role": "user", "content": req.message})
        reply = generate_reply(history)
        history.append({"role": "assistant", "content": reply})
        job_api_response["reply"] = reply;
        return job_api_response
    except Exception as e:
        logging.critical(
            f"Unhandled exception | session={req.session_id} | {str(e)}",
            exc_info=e
        )
        job_api_response["Message"] = "Internal server error"
        return JSONResponse(status_code=500, content=job_api_response)