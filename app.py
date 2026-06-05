import streamlit as st
from backend.database import init_db
from backend.auth import login_ui

st.set_page_config(
    page_title="ATS Resume Scorer",
    page_icon="🎯",
    layout="wide"
)

init_db()

if not login_ui():
    st.stop()

with st.sidebar:
    st.markdown(f"### 🎯 {st.session_state.get('name', 'User')}")
    st.caption(f"@{st.session_state.get('username', '')}")
    st.markdown("---")
    st.page_link("pages/1_Scorer.py",    label="📄  Resume Scorer")
    st.page_link("pages/2_Dashboard.py", label="📊  Dashboard")
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        for key in ["authenticated", "username", "name"]:
            st.session_state.pop(key, None)
        st.rerun()

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0a0a0f; color: #e8e8f0; }
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] { background: #0d0d14 !important; border-right: 1px solid #1a1a2a !important; }
[data-testid="stSidebarNavLink"] { border-radius: 10px !important; margin: 2px 8px !important; padding: 10px 16px !important; color: #4a4a60 !important; font-size: 12px !important; letter-spacing: 2px !important; text-transform: uppercase !important; font-weight: 700 !important; transition: all 0.2s !important; }
[data-testid="stSidebarNavLink"]:hover { background: #1a1a2a !important; color: #a78bfa !important; }
[data-testid="stSidebarNavLink"][aria-current="page"] { background: rgba(108,99,255,0.12) !important; color: #6c63ff !important; border-left: 2px solid #6c63ff !important; }

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #6c63ff, #a78bfa) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    font-size: 11px !important; padding: 14px 32px !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(108,99,255,0.4) !important;
}

@keyframes fadeUp { from { opacity:0; transform:translateY(28px); } to { opacity:1; transform:translateY(0); } }
@keyframes gradientShift { 0%,100% { background-position:0% 50%; } 50% { background-position:100% 50%; } }
@keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-10px); } }
@keyframes orb1 { 0%,100% { transform:translate(0,0) scale(1); } 33% { transform:translate(60px,-40px) scale(1.1); } 66% { transform:translate(-30px,50px) scale(0.95); } }
@keyframes orb2 { 0%,100% { transform:translate(0,0) scale(1); } 33% { transform:translate(-50px,60px) scale(1.05); } 66% { transform:translate(40px,-30px) scale(0.9); } }
@keyframes orb3 { 0%,100% { transform:translate(0,0) scale(1); } 50% { transform:translate(30px,40px) scale(1.08); } }
@keyframes particleDrift {
    0%   { transform: translateY(100vh) translateX(0px) rotate(0deg); opacity: 0; }
    10%  { opacity: 0.6; }
    90%  { opacity: 0.3; }
    100% { transform: translateY(-100px) translateX(80px) rotate(360deg); opacity: 0; }
}
@keyframes scanLine { 0% { transform: translateY(-100%); } 100% { transform: translateY(100vh); } }
@keyframes gridFade { 0%,100% { opacity:0.03; } 50% { opacity:0.06; } }

.bg-canvas {
    position: fixed; inset: 0; z-index: 0;
    pointer-events: none; overflow: hidden;
}
.orb {
    position: absolute; border-radius: 50%;
    filter: blur(80px); opacity: 0.18;
}
.orb-1 { width:600px; height:600px; background:radial-gradient(circle,#6c63ff,transparent); top:-100px; left:-100px; animation: orb1 12s ease-in-out infinite; }
.orb-2 { width:500px; height:500px; background:radial-gradient(circle,#a78bfa,transparent); bottom:-80px; right:-80px; animation: orb2 15s ease-in-out infinite; }
.orb-3 { width:400px; height:400px; background:radial-gradient(circle,#3b82f6,transparent); top:40%; left:40%; animation: orb3 18s ease-in-out infinite; }

.grid-bg {
    position: absolute; inset: 0;
    background-image: linear-gradient(rgba(108,99,255,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(108,99,255,0.06) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridFade 6s ease-in-out infinite;
}
.scan-line {
    position: absolute; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(108,99,255,0.15), rgba(167,139,250,0.2), rgba(108,99,255,0.15), transparent);
    animation: scanLine 8s linear infinite;
}

.particle { position: absolute; width: 3px; height: 3px; background: #6c63ff; border-radius: 50%; }

.hero-wrap {
    position: relative; z-index: 1;
    min-height: 82vh; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 60px 20px 40px;
}
.badge {
    display: inline-block; font-family: 'Syne', sans-serif;
    font-size: 10px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase;
    color: #6c63ff; border: 1px solid rgba(108,99,255,0.35);
    background: rgba(108,99,255,0.08); padding: 7px 20px;
    border-radius: 100px; margin-bottom: 32px;
    animation: fadeUp 0.5s ease both;
}
.hero-title {
    font-family: 'Syne', sans-serif; font-size: clamp(40px,6vw,76px);
    font-weight: 800; line-height: 1.08; color: #f0f0ff; margin-bottom: 24px;
    animation: fadeUp 0.5s ease 0.12s both;
}
.hero-title .grad {
    background: linear-gradient(135deg,#6c63ff,#a78bfa,#6c63ff);
    background-size: 200% 200%; -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 4s ease infinite;
}
.hero-sub {
    font-size: 16px; color: #6b6b80; max-width: 500px;
    line-height: 1.75; margin: 0 auto 16px;
    animation: fadeUp 0.5s ease 0.24s both;
}
.cards-row {
    display: flex; gap: 20px; justify-content: center;
    flex-wrap: wrap; margin-top: 60px;
    animation: fadeUp 0.5s ease 0.5s both;
}
.feature-card {
    background: rgba(17,17,24,0.85); backdrop-filter: blur(12px);
    border: 1px solid #1e1e2e; border-radius: 20px;
    padding: 32px 26px; width: 210px; text-align: left;
    transition: transform 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
    position: relative; overflow: hidden;
}
.feature-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg,#6c63ff,#a78bfa);
    transform: scaleX(0); transform-origin:left; transition: transform 0.35s ease;
}
.feature-card:hover { transform:translateY(-8px); border-color:rgba(108,99,255,0.45); box-shadow:0 24px 48px rgba(108,99,255,0.14); }
.feature-card:hover::before { transform:scaleX(1); }
.card-icon { font-size:30px; margin-bottom:16px; display:block; }
.card-icon.f1 { animation: float 3s ease-in-out infinite; }
.card-icon.f2 { animation: float 3s ease-in-out 0.5s infinite; }
.card-icon.f3 { animation: float 3s ease-in-out 1s infinite; }
.card-icon.f4 { animation: float 3s ease-in-out 1.5s infinite; }
.card-title { font-family:'Syne',sans-serif; font-size:14px; font-weight:700; color:#f0f0ff; margin-bottom:8px; }
.card-desc { font-size:12px; color:#4a4a60; line-height:1.65; }

.stat-strip {
    display:flex; gap:56px; justify-content:center; margin-top:64px;
    padding-top:40px; border-top:1px solid #1a1a2a;
    animation: fadeUp 0.5s ease 0.7s both;
}
.stat-item { text-align:center; }
.stat-num { font-family:'Syne',sans-serif; font-size:34px; font-weight:800; }
.stat-num .grad { background:linear-gradient(135deg,#6c63ff,#a78bfa); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.stat-label { font-size:10px; color:#4a4a60; letter-spacing:3px; text-transform:uppercase; margin-top:4px; }
</style>
""", unsafe_allow_html=True)

# ── Animated background ────────────────────────────────────────────────────────
st.markdown("""
<div class="bg-canvas">
    <div class="grid-bg"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="scan-line"></div>
    <div class="particle" style="left:10%;animation:particleDrift 9s linear 0s infinite"></div>
    <div class="particle" style="left:25%;animation:particleDrift 12s linear 1s infinite;background:#a78bfa"></div>
    <div class="particle" style="left:40%;animation:particleDrift 8s linear 3s infinite"></div>
    <div class="particle" style="left:55%;animation:particleDrift 14s linear 0.5s infinite;background:#a78bfa"></div>
    <div class="particle" style="left:70%;animation:particleDrift 10s linear 2s infinite"></div>
    <div class="particle" style="left:82%;animation:particleDrift 11s linear 4s infinite;background:#a78bfa"></div>
    <div class="particle" style="left:92%;animation:particleDrift 7s linear 1.5s infinite"></div>
</div>
""", unsafe_allow_html=True)

# ── Hero content ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="badge">✦ AI-Powered Resume Analysis</div>
    <div class="hero-title">Land More Interviews<br>with <span class="grad">Smarter</span> Resumes</div>
    <div class="hero-sub">Instantly score your resume against any job description. Know exactly what's missing, what matches, and how to fix it.</div>
    <div class="cards-row">
        <div class="feature-card">
            <span class="card-icon f1">⚡</span>
            <div class="card-title">Instant Score</div>
            <div class="card-desc">ATS score in seconds, powered by Llama 3.3 70B.</div>
        </div>
        <div class="feature-card">
            <span class="card-icon f2">🎯</span>
            <div class="card-title">Skill Gap Analysis</div>
            <div class="card-desc">See exactly which keywords are missing.</div>
        </div>
        <div class="feature-card">
            <span class="card-icon f3">📈</span>
            <div class="card-title">Track Progress</div>
            <div class="card-desc">Dashboard shows score improvement over time.</div>
        </div>
        <div class="feature-card">
            <span class="card-icon f4">🔒</span>
            <div class="card-title">Private & Secure</div>
            <div class="card-desc">Scans tied to your account only.</div>
        </div>
    </div>
    <div class="stat-strip">
        <div class="stat-item"><div class="stat-num"><span class="grad">100</span></div><div class="stat-label">Point Scale</div></div>
        <div class="stat-item"><div class="stat-num"><span class="grad">70B</span></div><div class="stat-label">Llama Model</div></div>
        <div class="stat-item"><div class="stat-num"><span class="grad">∞</span></div><div class="stat-label">Free Scans</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── CTA buttons using st.page_link (carries session state properly) ────────────
st.markdown("<div style='display:flex;justify-content:center;gap:16px;margin-top:8px;position:relative;z-index:1'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    if st.button("✦  Analyse Resume", use_container_width=True):
        st.switch_page("pages/1_Scorer.py")
with col3:
    if st.button("📊  Dashboard", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")
st.markdown("</div>", unsafe_allow_html=True)
