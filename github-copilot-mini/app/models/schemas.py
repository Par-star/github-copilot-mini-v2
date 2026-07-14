"""
Schemas - Request aur Response ka structure define karte hain.
Pydantic isse validation automatically kar deta hai (galat data aaya to error milega).
"""

from pydantic import BaseModel
from typing import Optional, List


class ExplainRequest(BaseModel):
    code: str                      # Jo code explain karna hai
    language: Optional[str] = "python"


class ExplainResponse(BaseModel):
    explanation: str


class GenerateRequest(BaseModel):
    description: str               # "Ek function chahiye jo..." wala natural language input
    language: Optional[str] = "python"
    style_notes: Optional[str] = None   # e.g. "use type hints", "keep it short"


class GenerateResponse(BaseModel):
    code: str


class ReviewPRRequest(BaseModel):
    owner: str                     # repo owner username
    repo: str                      # repo name
    pull_number: int                # PR number
    post_comment: Optional[bool] = False   # True -> GitHub par comment bhi post karega


class ReviewPRResponse(BaseModel):
    review: str
    files_reviewed: List[str]


class SuggestFixRequest(BaseModel):
    code: str
    error_message: str
    language: Optional[str] = "python"


class SuggestFixResponse(BaseModel):
    fix_explanation: str
    fixed_code: str
