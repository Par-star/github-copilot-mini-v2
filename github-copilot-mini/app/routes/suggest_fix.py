"""
Route: /suggest-fix
Feature: User apna failing code + error message de,
LLM root cause samjhaye aur fixed code de.
"""

import json
from fastapi import APIRouter
from app.models.schemas import SuggestFixRequest, SuggestFixResponse
from app.services.llm_service import call_llm

router = APIRouter()

SYSTEM_PROMPT = (
    "Tum ek debugging expert ho. User ka code aur error message dekhkar "
    "batao ki problem kya hai aur usse kaise fix karein. "
    "Respond ONLY in valid JSON with exactly two keys: "
    '"fix_explanation" (string) and "fixed_code" (string). '
    "Koi extra text, markdown, ya code fences mat do — sirf raw JSON."
)


@router.post("", response_model=SuggestFixResponse)
def suggest_fix(request: SuggestFixRequest):
    user_prompt = (
        f"Language: {request.language}\n\n"
        f"Code:\n{request.code}\n\n"
        f"Error Message:\n{request.error_message}"
    )
    raw_response = call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.2)

    # LLM kabhi-kabhi ```json fences laga deta hai, isliye clean karke parse karte hain
    cleaned = raw_response.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(cleaned)
        explanation = parsed.get("fix_explanation", "")
        fixed_code = parsed.get("fixed_code", "")
    except json.JSONDecodeError:
        # Fallback: agar JSON parse fail ho jaaye, to raw text hi de do
        explanation = raw_response
        fixed_code = ""

    return SuggestFixResponse(fix_explanation=explanation, fixed_code=fixed_code)
