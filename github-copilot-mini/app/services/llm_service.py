"""
LLM Service (Google Gemini)
----------------------------
Ye file LLM (Google Gemini) ke saath saari communication handle karti hai.
Har feature (explain, generate, review, fix) isi service ko use karta hai,
sirf alag-alag "prompt" bhejta hai.
"""

import os
import google.generativeai as genai

# API key environment variable se aayegi (.env file mein set karo)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")           # Chat/code ke liye
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/text-embedding-004")  # Vector DB ke liye


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    """
    Generic function jo koi bhi prompt LLM ko bhejti hai aur text response wapas deti hai.

    system_prompt -> LLM ko "role" batata hai (e.g. "tum ek senior code reviewer ho")
    user_prompt   -> actual task/question
    temperature   -> creativity control (kam = zyada predictable/accurate, jo code ke liye better hai)
    """
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=system_prompt,
    )
    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(temperature=temperature),
    )
    return response.text.strip()


def get_embedding(text: str) -> list[float]:
    """
    Text ko vector (numbers ki list) mein convert karta hai.
    Ye Vector DB mein store karne ke liye use hota hai (semantic search ke liye).
    """
    result = genai.embed_content(model=EMBEDDING_MODEL, content=text)
    return result["embedding"]
