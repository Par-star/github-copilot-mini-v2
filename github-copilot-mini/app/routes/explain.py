"""
Route: /explain
Feature: User code de, LLM use simple language mein explain kare.
"""

from fastapi import APIRouter
from app.models.schemas import ExplainRequest, ExplainResponse
from app.services.llm_service import call_llm

router = APIRouter()

SYSTEM_PROMPT = (
    "Tum ek expert senior software engineer ho jo code ko beginner-friendly "
    "tareeke se explain karte ho. Line-by-line nahi, balki logic aur purpose "
    "clearly samjhao. Agar koi potential bug ya bad practice dikhe, wo bhi mention karo."
)


@router.post("", response_model=ExplainResponse)
def explain_code(request: ExplainRequest):
    user_prompt = (
        f"Language: {request.language}\n\n"
        f"Ye code explain karo:\n```{request.language}\n{request.code}\n```"
    )
    explanation = call_llm(SYSTEM_PROMPT, user_prompt)
    return ExplainResponse(explanation=explanation)
