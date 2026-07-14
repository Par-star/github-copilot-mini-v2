"""
GitHub Copilot Mini - Main Application Entry Point
-----------------------------------------------------
Ye FastAPI app hai jo 4 core features expose karta hai:
1. /explain      -> Code explain karna
2. /generate     -> Function generate karna
3. /review-pr    -> GitHub PR review karna
4. /suggest-fix  -> Error/bug fix suggest karna
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import explain, generate, review_pr, suggest_fix

app = FastAPI(
    title="GitHub Copilot Mini",
    description="AI coding assistant: explain code, generate functions, review PRs, suggest fixes",
    version="1.0.0",
)

# CORS enable kiya taaki frontend (React/TS) backend ko call kar sake
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Har feature ka apna route file hai -> yahan register kar rahe hain
app.include_router(explain.router, prefix="/explain", tags=["Explain Code"])
app.include_router(generate.router, prefix="/generate", tags=["Generate Function"])
app.include_router(review_pr.router, prefix="/review-pr", tags=["Review PR"])
app.include_router(suggest_fix.router, prefix="/suggest-fix", tags=["Suggest Fix"])


@app.get("/")
def health_check():
    """Simple health check - server chal raha hai ya nahi, check karne ke liye"""
    return {"status": "ok", "message": "GitHub Copilot Mini is running 🚀"}
