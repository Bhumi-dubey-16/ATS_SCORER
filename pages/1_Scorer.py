import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.resume_parser import parse_resume
from backend.scorer import score_resume
from backend.database import save_result, init_db

# ── Auth guard ─────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    st.warning("Please login first.")
    st.stop()

username = st.session_state["username"]

st.set_page_config(page_title="ATS Scorer", page_icon="🎯", layout="wide")
init_db()


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0a0a0f; color: #e8e8f0; }
#MainMenu, footer, header { visibility: hidden; }

.hero-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px; font-weight: 700;
    letter-spacing: 4px; text-transform: uppercase;
    color: #6c63ff; margin-bottom: 12px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 48px; font-weight: 800; color: #f0f0ff; margin-bottom: 8px;
}
.hero-title span {
    background: linear-gradient(135deg, #6c63ff, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub { font-size: 14px; color: #4a4a60; margin-bottom: 40px; }

.upload-zone {
    background: #111118; border: 1px dashed #2a2a3d;
    border-radius: 16px; padding: 32px; margin-bottom: 16px;
    transition: border-color 0.2s;
}
.section-label {
    font-family: 'Syne', sans-serif; font-size: 10px;
    font-weight: 700; letter-spacing: 3px; text-transform: uppercase;
    color: #4a4a60; margin-bottom: 8px;
}

div[data-testid="stFileUploader"] {
    background: #111118 !important; border: 1px dashed #2a2a3d !important;
    border-radius: 16px !important; padding: 8px !important;
}
div[data-testid="stTextArea"] textarea {
    background: #111118 !important; border: 1px solid #1e1e2e !important;
    border-radius: 12px !important; color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 13px !important;
    resize: none !important;
}

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #6c63ff, #a78bfa) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; font-size: 11px !important;
    padding: 14px 32px !important; width: 100% !important;
    transition: opacity 0.2s !important;
}

.result-card {
    background: #111118; border: 1px solid #1e1e2e;
    border-radius: 16px; padding: 28px; margin-bottom: 16px;
    position: relative; overflow: hidden;
}
.result-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #6c63ff, #a78bfa);
}
.score-display {
    font-family: 'Syne', sans-serif; font-size: 72px; font-weight: 800;
    line-height: 1; text-align: center; margin: 16px 0;
}
.result-section-title {
    font-family: 'Syne', sans-serif; font-size: 10px; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase; color: #6c63ff; margin-bottom: 12px;
}
.skill-tag {
    display: inline-block;
    padding: 4px 14px; border-radius: 100px; font-size: 12px;
    font-weight: 500; margin: 3px;
}
.skill-match {
    background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2);
    color: #10b981;
}
.skill-miss {
    background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.15);
    color: #f87171;
}
.suggestion-item {
    background: #0d0d14; border-left: 2px solid #6c63ff;
    border-radius: 0 8px 8px 0; padding: 10px 16px;
    margin-bottom: 8px; font-size: 13px; color: #c8c8e0;
}

[data-testid="stSidebar"] { background: #0d0d14 !important; border-right: 1px solid #1a1a2a !important; }
[data-testid="stSidebarNavLink"] {
    border-radius: 10px !important; margin: 2px 8px !important;
    padding: 10px 16px !important; color: #4a4a60 !important;
    font-size: 12px !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; font-weight: 700 !important;
}
[data-testid="stSidebarNavLink"]:hover { background: #1a1a2a !important; color: #a78bfa !important; }
[data-testid="stSidebarNavLink"][aria-current="page"] {
    background: rgba(108,99,255,0.12) !important; color: #6c63ff !important;
    border-left: 2px solid #6c63ff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-label">AI-Powered Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Resume <span>Scorer</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Upload your resume and paste a job description to get your ATS score instantly.</div>', unsafe_allow_html=True)

# ── Inputs ─────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-label">Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf", "docx"], label_visibility="collapsed")

with col_right:
    st.markdown('<div class="section-label">Job Description</div>', unsafe_allow_html=True)
    job_desc = st.text_area("", height=180, placeholder="Paste the full job description here...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
analyse_btn = st.button("✦  Analyse Resume")

# ── Analysis ───────────────────────────────────────────────────────────────────
if analyse_btn:
    if not uploaded_file:
        st.error("Please upload a resume (PDF or DOCX).")
    elif not job_desc.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Analysing your resume against the job description..."):
            resume_text = parse_resume(uploaded_file, uploaded_file.name)
            result = score_resume(resume_text, job_desc)

        # Save with username
        save_result(
            username        = username,
            resume_filename = uploaded_file.name,
            job_description = job_desc,
            result_dict     = result
        )

        score = result.get("score", 0)
        if score >= 70:
            score_color = "#10b981"
        elif score >= 50:
            score_color = "#f59e0b"
        else:
            score_color = "#ef4444"

        # ── Score card ─────────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="result-card" style="text-align:center">
            <div class="result-section-title">ATS Score</div>
            <div class="score-display" style="color:{score_color}">{int(score)}<span style="font-size:24px;color:#4a4a60">/100</span></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Skills columns ─────────────────────────────────────────────────────
        r1, r2 = st.columns(2, gap="large")

        with r1:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-section-title">✅ Matching Skills</div>', unsafe_allow_html=True)
            tags = "".join([f'<span class="skill-tag skill-match">{s}</span>' for s in result.get("matching_skills", [])])
            st.markdown(tags or "<p style='color:#4a4a60;font-size:13px'>None found.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with r2:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-section-title">❌ Missing Keywords</div>', unsafe_allow_html=True)
            tags = "".join([f'<span class="skill-tag skill-miss">{k}</span>' for k in result.get("missing_keywords", [])])
            st.markdown(tags or "<p style='color:#4a4a60;font-size:13px'>None missing — great match!</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Suggestions ────────────────────────────────────────────────────────
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-section-title">💡 Suggestions</div>', unsafe_allow_html=True)
        for s in result.get("suggestions", []):
            st.markdown(f'<div class="suggestion-item">→ {s}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Summary ────────────────────────────────────────────────────────────
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-section-title">📝 Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:14px;color:#c8c8e0;line-height:1.7">{result.get("summary","")}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
