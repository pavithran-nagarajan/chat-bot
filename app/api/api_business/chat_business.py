import os
from dotenv import load_dotenv
from app.api.api_business.model_business import llm

load_dotenv()

def generate_reply(messages: list[dict]) -> str:
    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=int(os.getenv("MAX_TOKENS", 512)),
        temperature=float(os.getenv("TEMPERATURE", 0.7)),
    )
    return response["choices"][0]["message"]["content"]