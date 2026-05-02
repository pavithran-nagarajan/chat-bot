# 🤖 Chat Bot - Llama 3.1 8B

A local AI chatbot built with FastAPI and Llama 3.1 8B model.

---

## 📋 Prerequisites

- Python 3.10+
- 8GB RAM minimum
- Windows / Mac / Linux

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone chat-bot
cd chat-bot
```

---

### 2. Create virtual environment

```bash
python -m venv venv
```

**Activate:**

```bash
# Windows
.\venv\Scripts\Activate.ps1

# Mac / Linux
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Download the model

```bash
python download_script\download.py
```

---

### 5. Create your `.env` file

Make sure you are inside the `CHAT-BOT/` folder, then run:

```bash
NEW-ITEM .env
```

Open `.env` and add the following config:

```env
MODEL_PATH=./models/llama-3.1-8B/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
N_CTX=4096
N_GPU_LAYERS=0
TEMPERATURE=0.7
MAX_TOKENS=512
HOST=127.0.0.1
PORT=8000
UPLOAD_PATH=upload
```

---

### 6. Run the app

```bash
uvicorn main:app --reload
```

---

## 🔗 API Endpoints

| Description        | URL                          |
|--------------------|------------------------------|
| Interactive API docs | http://127.0.0.1:8000/docs |