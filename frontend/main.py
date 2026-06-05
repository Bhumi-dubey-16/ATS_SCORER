import streamlit as st
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.resume_parser import parse_resume
from backend.scorer import score_resume
from backend.database import init_db, save_result

st.set_page_config(
    page_title="ATS Resume Scorer",
    page_icon="📄",
    layout="centered"
)

init_db()

st.page_link("frontend/dashboard.py", label="📊 View your progress dashboard →")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Hide streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

.hero-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #6c63ff;
    margin-bottom: 12px;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 52px;
    font-weight: 800;
    line-height: 1.1;
    color: #f0f0ff;
    margin-bottom: 16px;
}

.hero-title span {
    background: linear-gradient(135deg, #6c63ff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 15px;
    color: #6b6b80;
    font-weight: 300;
    margin-bottom: 48px;
    line-height: 1.6;
}

.upload-zone {
    border: 1.5px dashed #2a2a3d;
    border-radius: 16px;
    padding: 32px;
    background: #111118;
    transition: border-color 0.3s;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4a4a60;
    margin-bottom: 8px;
    font-weight: 600;
}

/* Input styling */
.stTextArea textarea {
    background: #111118 !important;
    border: 1.5px solid #1e1e2e !important;
    border-radius: 12px !important;
    color: #c8c8e0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 16px !important;
    resize: none !important;
}

.stTextArea textarea:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.1) !important;
}

.stFileUploader {
    background: #111118 !important;
    border: 1.5px solid #1e1e2e !important;
    border-radius: 12px !important;
    padding: 8px !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #6c63ff 0%, #a78bfa 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 16px 32px !important;
    height: 56px !important;
    transition: all 0.3s !important;
    box-shadow: 0 8px 32px rgba(108, 99, 255, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(108, 99, 255, 0.5) !important;
}

/* Score card */
.score-card {
    background: linear-gradient(135deg, #13131f 0%, #1a1a2e 100%);
    border: 1px solid #2a2a3d;
    border-radius: 20px;
    padding: 40px;
    margin: 32px 0 24px;
    position: relative;
    overflow: hidden;
}

.score-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6c63ff, #a78bfa, #6c63ff);
}

.score-eyebrow {
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #4a4a60;
    margin-bottom: 8px;
}

.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 88px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 4px;
}

.score-denom {
    font-size: 13px;
    color: #4a4a60;
    letter-spacing: 1px;
}

.score-bar-bg {
    background: #1e1e2e;
    border-radius: 100px;
    height: 6px;
    margin-top: 24px;
    overflow: hidden;
}

.score-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 1s ease;
}

/* Summary box */
.summary-box {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-left: 3px solid #6c63ff;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 24px 0;
    font-size: 14px;
    color: #9090b0;
    line-height: 1.7;
}

/* Tags */
.tag-green {
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.2);
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px;
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.3px;
}

.tag-red {
    background: rgba(239, 68, 68, 0.08);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.15);
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px;
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 0.3px;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #e8e8f0;
    margin: 32px 0 16px;
}

.suggestion-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: flex-start;
    gap: 14px;
}

.suggestion-num {
    background: linear-gradient(135deg, #6c63ff, #a78bfa);
    color: white;
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 800;
    width: 24px;
    height: 24px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
}

.suggestion-text {
    font-size: 13px;
    color: #9090b0;
    line-height: 1.6;
}

.divider {
    border: none;
    border-top: 1px solid #1a1a2a;
    margin: 40px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────
st.markdown('<div class="hero-label">AI-Powered Career Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Resume<br><span>ATS Scorer</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Instantly know how your resume performs against any job description.<br>Find gaps. Fix them. Land interviews.</div>', unsafe_allow_html=True)

# ── Inputs ─────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-label">Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="section-label">Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "JD",
        height=160,
        placeholder="Paste the full job description here...",
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
analyse = st.button("ANALYSE RESUME →", use_container_width=True)

# ── On Analyse ─────────────────────────────────────────────
if analyse:

    if not uploaded_file:
        st.error("Upload a resume to continue.")
        st.stop()

    if not job_description.strip():
        st.error("Paste a job description to continue.")
        st.stop()

    with st.spinner("Extracting resume text..."):
        resume_text = parse_resume(uploaded_file, uploaded_file.name)

    if not resume_text:
        st.error("Could not read that file. Please upload a PDF or Word document.")
        st.stop()

    with st.spinner("Scoring with AI..."):
        raw_result = score_resume(resume_text, job_description)

    try:
        result = json.loads(raw_result)
    except json.JSONDecodeError:
        st.error("Unexpected response from AI. Please try again.")
        st.stop()

    save_result(uploaded_file.name, job_description, result)

    # ── Score card ─────────────────────────────────────────
    score = result.get("score", 0)

    if score >= 70:
        score_color = "#10b981"
        score_label = "Strong Match"
    elif score >= 50:
        score_color = "#f59e0b"
        score_label = "Moderate Match"
    else:
        score_color = "#ef4444"
        score_label = "Weak Match"

    st.markdown(f"""
    <div class="score-card">
        <div class="score-eyebrow">ATS Match Score</div>
        <div class="score-number" style="color:{score_color}">{score}</div>
        <div class="score-denom">out of 100 &nbsp;·&nbsp; <span style="color:{score_color}">{score_label}</span></div>
        <div class="score-bar-bg">
            <div class="score-bar-fill" style="width:{score}%; background:linear-gradient(90deg, {score_color}99, {score_color});"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary ────────────────────────────────────────────
    st.markdown(f'<div class="summary-box">{result.get("summary", "")}</div>', unsafe_allow_html=True)

    # ── Skills ─────────────────────────────────────────────
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown('<div class="section-title">✦ Matching Skills</div>', unsafe_allow_html=True)
        skills = result.get("matching_skills", [])
        if skills:
            st.markdown(" ".join([f'<span class="tag-green">{s}</span>' for s in skills]), unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#4a4a60;font-size:13px">None found</span>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-title">✦ Missing Keywords</div>', unsafe_allow_html=True)
        missing = result.get("missing_keywords", [])
        if missing:
            st.markdown(" ".join([f'<span class="tag-red">{s}</span>' for s in missing]), unsafe_allow_html=True)
        else:
            st.markdown('<span style="color:#4a4a60;font-size:13px">None — perfect match</span>', unsafe_allow_html=True)

    # ── Suggestions ────────────────────────────────────────
    st.markdown('<div class="section-title">✦ How to Improve</div>', unsafe_allow_html=True)
    for i, s in enumerate(result.get("suggestions", []), 1):
        st.markdown(f"""
        <div class="suggestion-card">
            <div class="suggestion-num">{i}</div>
            <div class="suggestion-text">{s}</div>
        </div>
        """, unsafe_allow_html=True)

