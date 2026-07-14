"""
GitHub Copilot Mini - Frontend (Pure Python using Streamlit)
--------------------------------------------------------------
Ye ek Python-only frontend hai — koi HTML/CSS/JS nahi likha,
Streamlit khud UI render karta hai.

Ye backend (FastAPI) ko HTTP requests bhejta hai using `requests` library.

Run karne ke liye:
    streamlit run frontend/app.py
"""

import streamlit as st
import requests

# Backend ka base URL (jab tum backend run karoge to ye address hoga)
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="GitHub Copilot Mini", page_icon="🤖", layout="wide")

st.title("🤖 GitHub Copilot Mini")
st.caption("AI coding assistant — explain, generate, review PRs, aur fix suggest kare")

# Sidebar mein feature select karne ka option
feature = st.sidebar.radio(
    "Feature chuno:",
    ["📝 Explain Code", "⚡ Generate Function", "🔍 Review PR", "🛠️ Suggest Fix"],
)

st.sidebar.markdown("---")
st.sidebar.info("Backend chal raha hona chahiye:\n`uvicorn app.main:app --reload`")


# ---------------------------------------------------------
# Feature 1: Explain Code
# ---------------------------------------------------------
if feature == "📝 Explain Code":
    st.header("📝 Explain Code")
    language = st.selectbox("Language", ["python", "javascript", "typescript", "java", "c++", "go"])
    code = st.text_area("Apna code yahan paste karo:", height=250, placeholder="def add(a, b):\n    return a + b")

    if st.button("Explain karo", type="primary"):
        if not code.strip():
            st.warning("Pehle code paste karo!")
        else:
            with st.spinner("LLM code samajh raha hai..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/explain",
                        json={"code": code, "language": language},
                        timeout=60,
                    )
                    response.raise_for_status()
                    result = response.json()
                    st.success("Explanation ready!")
                    st.markdown(result["explanation"])
                except Exception as e:
                    st.error(f"Error: {e}")


# ---------------------------------------------------------
# Feature 2: Generate Function
# ---------------------------------------------------------
elif feature == "⚡ Generate Function":
    st.header("⚡ Generate Function")
    language = st.selectbox("Language", ["python", "javascript", "typescript", "java", "c++", "go"])
    description = st.text_area(
        "Kya function chahiye, bataye:",
        height=150,
        placeholder="Ek function jo list ke saare even numbers filter kare",
    )
    style_notes = st.text_input("Extra style notes (optional):", placeholder="e.g. use type hints")

    if st.button("Generate karo", type="primary"):
        if not description.strip():
            st.warning("Pehle description likho!")
        else:
            with st.spinner("Code generate ho raha hai..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json={
                            "description": description,
                            "language": language,
                            "style_notes": style_notes or None,
                        },
                        timeout=60,
                    )
                    response.raise_for_status()
                    result = response.json()
                    st.success("Code generate ho gaya!")
                    st.code(result["code"], language=language)
                except Exception as e:
                    st.error(f"Error: {e}")


# ---------------------------------------------------------
# Feature 3: Review PR
# ---------------------------------------------------------
elif feature == "🔍 Review PR":
    st.header("🔍 Review GitHub Pull Request")
    col1, col2, col3 = st.columns(3)
    with col1:
        owner = st.text_input("Repo Owner", placeholder="octocat")
    with col2:
        repo = st.text_input("Repo Name", placeholder="hello-world")
    with col3:
        pull_number = st.number_input("PR Number", min_value=1, step=1)

    post_comment = st.checkbox("Review ko GitHub PR par comment ke roop mein post karo")

    if st.button("Review karo", type="primary"):
        if not owner or not repo:
            st.warning("Repo owner aur name dono zaroori hain!")
        else:
            with st.spinner("PR fetch aur review ho raha hai..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/review-pr",
                        json={
                            "owner": owner,
                            "repo": repo,
                            "pull_number": int(pull_number),
                            "post_comment": post_comment,
                        },
                        timeout=90,
                    )
                    response.raise_for_status()
                    result = response.json()
                    st.success(f"{len(result['files_reviewed'])} files review hui!")
                    st.write("**Files:**", ", ".join(result["files_reviewed"]))
                    st.markdown("### Review")
                    st.markdown(result["review"])
                except Exception as e:
                    st.error(f"Error: {e}")


# ---------------------------------------------------------
# Feature 4: Suggest Fix
# ---------------------------------------------------------
elif feature == "🛠️ Suggest Fix":
    st.header("🛠️ Suggest Fix")
    language = st.selectbox("Language", ["python", "javascript", "typescript", "java", "c++", "go"])
    code = st.text_area("Failing code:", height=200, placeholder="print(x)")
    error_message = st.text_area("Error message:", height=100, placeholder="NameError: x is not defined")

    if st.button("Fix suggest karo", type="primary"):
        if not code.strip() or not error_message.strip():
            st.warning("Code aur error message dono zaroori hain!")
        else:
            with st.spinner("Fix dhoondha ja raha hai..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/suggest-fix",
                        json={"code": code, "error_message": error_message, "language": language},
                        timeout=60,
                    )
                    response.raise_for_status()
                    result = response.json()
                    st.success("Fix mil gaya!")
                    st.markdown("### Explanation")
                    st.markdown(result["fix_explanation"])
                    if result["fixed_code"]:
                        st.markdown("### Fixed Code")
                        st.code(result["fixed_code"], language=language)
                except Exception as e:
                    st.error(f"Error: {e}")
