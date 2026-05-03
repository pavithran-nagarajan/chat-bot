from llama_cpp import Llama
from app.business.common_business.get_env_business import get_env

def get_reply_from_llm(messages_with_context: list[dict]) -> str:
    llm = Llama(
        model_path=get_env("MODEL_PATH"),
        n_ctx=int(get_env("N_CTX", 4096)),
        n_gpu_layers=int(get_env("N_GPU_LAYERS", 0)),
    )

    response = llm.create_chat_completion(
        messages=messages_with_context,
        max_tokens=int(get_env("MAX_TOKENS", 512)),
        temperature=float(get_env("TEMPERATURE", 0.7)),
    )
    return response["choices"][0]["message"]["content"]