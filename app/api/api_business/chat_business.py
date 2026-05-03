from app.api.api_business.rag_business import search_documents
from app.business.model_business.llama_business import get_reply_from_llm

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
    
    response = get_reply_from_llm(messages_with_context)
    return response