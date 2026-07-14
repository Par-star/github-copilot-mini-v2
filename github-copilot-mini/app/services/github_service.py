"""
GitHub Service
--------------
Ye file GitHub API se baat karti hai:
1. PR ke files/diff fetch karna
2. PR par review comment post karna

Authentication: GitHub Personal Access Token (.env mein GITHUB_TOKEN)
"""

import os
import httpx

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


async def get_pr_files(owner: str, repo: str, pull_number: int) -> list[dict]:
    """
    PR ke andar jitni files change hui hain, unka diff/patch fetch karta hai.
    Return: [{filename, patch, additions, deletions}, ...]
    """
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pull_number}/files"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()


async def post_pr_comment(owner: str, repo: str, pull_number: int, comment_body: str) -> dict:
    """
    PR par ek comment post karta hai (jaise ek human reviewer karta hai).
    Note: 'issues' endpoint use hota hai kyunki GitHub mein har PR ek issue bhi hoti hai.
    """
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues/{pull_number}/comments"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HEADERS, json={"body": comment_body})
        response.raise_for_status()
        return response.json()


def build_diff_summary(files: list[dict]) -> str:
    """
    Saari files ke diffs ko ek readable text mein combine karta hai,
    taaki LLM ko ek hi prompt mein diya ja sake.
    """
    summary_parts = []
    for file in files:
        filename = file.get("filename")
        patch = file.get("patch", "(binary file or no diff available)")
        summary_parts.append(f"### File: {filename}\n```diff\n{patch}\n```")
    return "\n\n".join(summary_parts)
