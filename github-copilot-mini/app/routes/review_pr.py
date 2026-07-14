"""
Route: /review-pr
Feature: GitHub PR ka diff fetch karo, LLM se review karwao,
aur (optional) review ko PR par comment ke roop mein post kar do.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ReviewPRRequest, ReviewPRResponse
from app.services.github_service import get_pr_files, build_diff_summary, post_pr_comment
from app.services.llm_service import call_llm

router = APIRouter()

SYSTEM_PROMPT = (
    "Tum ek senior code reviewer ho. Diye gaye PR diff ko review karo. "
    "In cheezon par focus karo: bugs, security issues, code style, "
    "performance, aur best practices. Har issue ke liye file/line reference do. "
    "Agar sab sahi hai to bhi honestly bolo 'looks good'."
)


@router.post("", response_model=ReviewPRResponse)
async def review_pull_request(request: ReviewPRRequest):
    try:
        files = await get_pr_files(request.owner, request.repo, request.pull_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"GitHub se PR fetch nahi hua: {e}")

    if not files:
        raise HTTPException(status_code=404, detail="Is PR mein koi file changes nahi mile")

    diff_summary = build_diff_summary(files)
    review_text = call_llm(SYSTEM_PROMPT, diff_summary)

    if request.post_comment:
        await post_pr_comment(request.owner, request.repo, request.pull_number, review_text)

    return ReviewPRResponse(
        review=review_text,
        files_reviewed=[f["filename"] for f in files],
    )
