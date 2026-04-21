import os
from dotenv import load_dotenv
from llama_cpp import Llama

load_dotenv()  # reads your .env file automatically

llm = Llama(
    model_path=os.getenv("MODEL_PATH"),
    n_ctx=int(os.getenv("N_CTX", 4096)),
    n_gpu_layers=int(os.getenv("N_GPU_LAYERS", 0)),
)