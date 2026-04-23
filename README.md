# 🤖 Chat Bot - Llama 3.1 8B

A local AI chatbot built with FastAPI and Llama 3.1 8B model.

## 📋 Prerequisites
- Python 3.10+
- 8GB RAM minimum
- Windows/Mac/Linux

## 🚀 Getting Started

### 1. Clone the repository
git clone your-repo-url
cd chat-bot

### 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

### 3. Install dependencies
pip install -r requirements.txt

### 4. Download the model
python download_script\download.py

### 5. Create .env file
Copy .env.example to .env and fill in values:
MODEL_PATH=./models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
N_CTX=4096
N_GPU_LAYERS=0
TEMPERATURE=0.7
MAX_TOKENS=512

### 6. Run the app
uvicorn main:app --reload

## 🔗 API Endpoints
|http://127.0.0.1:8000/docs
