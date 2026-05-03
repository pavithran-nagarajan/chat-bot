from fastapi import APIRouter
from pydantic import BaseModel
from app.api.api_business.chat_business import generate_reply
from app.business.common_business.exception_handler_business import handle_exception

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
        handle_exception(e, context="extract_text")