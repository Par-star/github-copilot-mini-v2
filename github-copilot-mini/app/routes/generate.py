"""
Route: /generate
Feature: User natural language mein bataye "kya function chahiye",
LLM usko actual working code mein convert kare.
"""

from fastapi import APIRouter
from app.models.schemas import GenerateRequest, GenerateResponse
from app.services.llm_service import call_llm

router = APIRouter()

SYSTEM_PROMPT = (
    "Tum ek expert software engineer ho. User jo function maangega, "
    "uska clean, production-quality code likho. Sirf code do, extra "
    "conversation nahi. Zaroori comments add karo agar logic complex ho."
)


@router.post("", response_model=GenerateResponse)
def generate_function(request: GenerateRequest):
    user_prompt = (
        f"Language: {request.language}\n"
        f"Style notes: {request.style_notes or 'none'}\n\n"
        f"Task: {request.description}"
    )
    code = call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.2)
    return GenerateResponse(code=code)
