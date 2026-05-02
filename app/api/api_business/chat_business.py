import os
from dotenv import load_dotenv
from app.business.model_business.model_business import llm
from app.api.api_business.rag_business import search_documents

load_dotenv()

def generate_reply(messages: list[dict]) -> str:
    # Get last user message
    user_message = messages[-1]["content"]
    
    # Search relevant documents
    context = search_documents(user_message)
    
    # Add context to system message
    messages_with_context = [
        {
            "role": "system",
            "content": f"You are a helpful assistant. Use this context to answer:\n{context}"
        }
    ] + messages[1:]  # skip original system message
    
    response = llm.create_chat_completion(
        messages=messages_with_context,
        max_tokens=int(os.getenv("MAX_TOKENS", 512)),
        temperature=float(os.getenv("TEMPERATURE", 0.7)),
    )
    return response["choices"][0]["message"]["content"]