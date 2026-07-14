# GitHub Copilot Mini 🚀

AI coding assistant jo code explain karta hai, functions generate karta hai,
GitHub PRs review karta hai, aur bug fixes suggest karta hai.

**Tech Stack:** 100% Python — Backend: FastAPI | Frontend: Streamlit | LLM: Google Gemini | Vector DB: ChromaDB | GitHub API: httpx

## Features
| Endpoint | Kaam |
|---|---|
| `POST /explain` | Code ko simple language mein explain karta hai |
| `POST /generate` | Description se function code generate karta hai |
| `POST /review-pr` | GitHub PR ka diff fetch karke AI review deta hai |
| `POST /suggest-fix` | Error message dekh kar fix suggest karta hai |

## Setup

```bash
# 1. Virtual environment banao
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Dependencies install karo
pip install -r requirements.txt

# 3. .env file banao
cp .env.example .env
# .env mein apni OPENAI_API_KEY aur GITHUB_TOKEN daalo

# 4. Backend server run karo (Terminal 1)
uvicorn app.main:app --reload

# 5. Frontend run karo (Terminal 2, naya terminal window)
streamlit run frontend/app.py
```

Backend chalega: `http://localhost:8000`
Interactive API docs: `http://localhost:8000/docs`
Frontend (Streamlit UI) chalega: `http://localhost:8501`

> **Note:** Backend aur Frontend dono ko **alag-alag terminal** mein, **saath mein** chalana hai. Ye poora project **100% Python** mein bana hai — backend FastAPI hai, frontend Streamlit hai, koi HTML/CSS/JS nahi likha gaya.

## Example Requests

### Explain Code
```bash
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d '{"code": "def add(a,b): return a+b", "language": "python"}'
```

### Generate Function
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "ek function jo list ke saare even numbers filter kare"}'
```

### Review PR
```bash
curl -X POST http://localhost:8000/review-pr \
  -H "Content-Type: application/json" \
  -d '{"owner": "octocat", "repo": "hello-world", "pull_number": 1}'
```

### Suggest Fix
```bash
curl -X POST http://localhost:8000/suggest-fix \
  -H "Content-Type: application/json" \
  -d '{"code": "print(x)", "error_message": "NameError: x is not defined"}'
```
