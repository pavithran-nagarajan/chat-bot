from fastapi import APIRouter
from pydantic import BaseModel
from app.api.api_business.chat_business import generate_reply

router = APIRouter()
sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/chat")
def chat_endpoint(req: ChatRequest):
    history = sessions.setdefault(req.session_id, [
        {"role": "system", "content": "You are a helpful assistant."}
    ])
    history.append({"role": "user", "content": req.message})
    reply = generate_reply(history)
    history.append({"role": "assistant", "content": reply})
    return {"reply": reply}