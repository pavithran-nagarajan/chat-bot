import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.api_controller.chat_controller import router as chat_router

load_dotenv()

app = FastAPI()

# Register all controllers here
app.include_router(chat_router)