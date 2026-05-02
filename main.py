import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.api_controller.chat_controller import router as chat_router
from app.api.api_controller.rag_controller import router as rag_router
from app.business.common_business.logging_business import setup_logging

load_dotenv()

app = FastAPI()

# Register all controllers here
app.include_router(chat_router)
app.include_router(rag_router)

# Initialize necessary modules here
setup_logging()