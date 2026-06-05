import streamlit as st
import sys, os
import json
from collections import Counter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import init_db, get_history

# ── Auth guard ─────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    st.warning("Please login first.")
    st.stop()

username = st.session_state["username"]

st.set_page_config(page_title="ATS Dashboard", page_icon="📊", layout="wide")
init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0a0a0f; color: #e8e8f0; }
#MainMenu, footer, header { visibility: hidden; }

.hero-label { font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: #6c63ff; margin-bottom: 12px; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 42px; font-weight: 800; color: #f0f0ff; margin-bottom: 8px; }
.hero-title span { background: linear-gradient(135deg, #6c63ff, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { font-size: 14px; color: #4a4a60; margin-bottom: 40px; }

.stat-card { background: #111118; border: 1px solid #1e1e2e; border-radius: 16px; padding: 24px 28px; position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #6c63ff, #a78bfa); }
.stat-eyebrow { font-family: 'Syne', sans-serif; font-size: 9px; letter-spacing: 3px; text-transform: uppercase; color: #4a4a60; margin-bottom: 8px; }
.stat-value { font-family: 'Syne', sans-serif; font-size: 40px; font-weight: 800; line-height: 1; color: #f0f0ff; }
.stat-sub { font-size: 12px; color: #4a4a60; margin-top: 4px; }

.section-title { font-family: 'Syne', sans-serif; font-size: 12px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #6c63ff; margin: 40px 0 20px; }

.gap-row { background: #111118; border: 1px solid #1e1e2e; border-radius: 12px; padding: 14px 20px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; }
.gap-skill { font-size: 14px; color: #c8c8e0; font-weight: 500; }
.gap-count { font-family: 'Syne', sans-serif; font-size: 11px; font-weight: 700; color: #f87171; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.15); padding: 3px 12px; border-radius: 100px; letter-spacing: 1px; }
.gap-bar-bg { background: #1e1e2e; border-radius: 100px; height: 3px; width: 120px; overflow: hidden; margin-left: 16px; }

.scan-row { background: #111118; border: 1px solid #1e1e2e; border-radius: 12px; padding: 16px 24px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; }
.scan-filename { font-size: 13px; color: #c8c8e0; font-weight: 500; flex: 1; }
.scan-date { font-size: 11px; color: #4a4a60; margin: 0 24px; }
.scan-score { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800; min-width: 48px; text-align: right; }

.empty-state { text-align: center; padding: 80px 40px; color: #4a4a60; }
.empty-state-icon { font-size: 48px; margin-bottom: 16px; }
.empty-state-title { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 700; color: #2a2a3d; margin-bottom: 8px; }
.empty-state-sub { font-size: 13px; color: #3a3a50; }

[data-testid="stSidebar"] { background: #0d0d14 !important; border-right: 1px solid #1a1a2a !important; }
[data-testid="stSidebarNavLink"] { border-radius: 10px !important; margin: 2px 8px !important; padding: 10px 16px !important; color: #4a4a60 !important; font-size: 12px !important; letter-spacing: 2px !important; text-transform: uppercase !important; font-weight: 700 !important; transition: all 0.2s !important; }
[data-testid="stSidebarNavLink"]:hover { background: #1a1a2a !important; color: #a78bfa !important; }
[data-testid="stSidebarNavLink"][aria-current="page"] { background: rgba(108,99,255,0.12) !important; color: #6c63ff !important; border-left: 2px solid #6c63ff !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-label">Personal Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Your <span>Progress</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Track how your resume improves across every application.</div>', unsafe_allow_html=True)

# ── Load data — filtered by logged-in user ─────────────────────────────────────
history = get_history(username=username, limit=50)

if not history:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">📭</div>
        <div class="empty-state-title">No scans yet</div>
        <div class="empty-state-sub">Go to the scorer, upload a resume and analyse it.<br>Your results will appear here.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Stat cards ─────────────────────────────────────────────────────────────────
scores = [h["score"] for h in history]
avg_score    = round(sum(scores) / len(scores), 1)
best_score   = max(scores)
latest_score = scores[0]
trend        = latest_score - scores[1] if len(scores) > 1 else 0
trend_str    = f"+{round(trend,1)}" if trend >= 0 else str(round(trend,1))

c1, c2, c3, c4 = st.columns(4, gap="medium")

with c1:
    st.markdown(f"""<div class="stat-card"><div class="stat-eyebrow">Total Scans</div><div class="stat-value">{len(history)}</div><div class="stat-sub">resumes analysed</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="stat-card"><div class="stat-eyebrow">Average Score</div><div class="stat-value">{avg_score}</div><div class="stat-sub">across all scans</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="stat-card"><div class="stat-eyebrow">Best Score</div><div class="stat-value" style="color:#10b981">{best_score}</div><div class="stat-sub">personal best</div></div>""", unsafe_allow_html=True)
with c4:
    trend_color = "#10b981" if trend >= 0 else "#ef4444"
    st.markdown(f"""<div class="stat-card"><div class="stat-eyebrow">Latest Trend</div><div class="stat-value" style="color:{trend_color}">{trend_str}</div><div class="stat-sub">vs previous scan</div></div>""", unsafe_allow_html=True)

# ── Score progression chart ────────────────────────────────────────────────────
st.markdown('<div class="section-title">✦ Score Progression</div>', unsafe_allow_html=True)

import plotly.graph_objects as go

chart_data = list(reversed(history))
x_labels   = [f"Scan {i+1}" for i in range(len(chart_data))]
y_values   = [h["score"] for h in chart_data]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x_labels, y=y_values,
    mode="lines+markers",
    line=dict(color="#6c63ff", width=2.5, shape="spline"),
    marker=dict(size=8, color="#6c63ff", line=dict(color="#a78bfa", width=2)),
    fill="tozeroy", fillcolor="rgba(108,99,255,0.06)",
    hovertemplate="<b>%{x}</b><br>Score: %{y}<extra></extra>"
))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#6b6b80", size=12),
    margin=dict(l=0, r=0, t=8, b=0), height=260,
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#4a4a60", size=11)),
    yaxis=dict(showgrid=True, gridcolor="#1a1a2a", zeroline=False, range=[0,105], tickfont=dict(color="#4a4a60", size=11)),
    hoverlabel=dict(bgcolor="#1a1a2e", bordercolor="#6c63ff", font=dict(color="#e8e8f0"))
)
st.plotly_chart(fig, use_container_width=True)

# ── Two column layout ──────────────────────────────────────────────────────────
left, right = st.columns([1,1], gap="large")

with left:
    st.markdown('<div class="section-title">✦ Recurring Skill Gaps</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:12px;color:#4a4a60;margin-bottom:16px">Keywords missing across multiple scans — fix these first.</p>', unsafe_allow_html=True)

    all_missing = []
    for h in history:
        all_missing.extend(h["missing_keywords"])

    if all_missing:
        gap_counts = Counter(all_missing).most_common(8)
        max_count  = gap_counts[0][1]
        for skill, count in gap_counts:
            bar_width = int((count / max_count) * 100)
            label = f"missing in {count} scan{'s' if count > 1 else ''}"
            st.markdown(f"""
            <div class="gap-row">
                <div class="gap-skill">{skill}</div>
                <div style="display:flex;align-items:center;gap:12px">
                    <div class="gap-bar-bg">
                        <div style="height:100%;width:{bar_width}%;background:linear-gradient(90deg,#ef444480,#ef4444);border-radius:100px;"></div>
                    </div>
                    <div class="gap-count">{label}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#4a4a60;font-size:13px">No recurring gaps found yet.</p>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-title">✦ Recent Scans</div>', unsafe_allow_html=True)
    for h in history[:10]:
        score = h["score"]
        score_color = "#10b981" if score >= 70 else ("#f59e0b" if score >= 50 else "#ef4444")
        st.markdown(f"""
        <div class="scan-row">
            <div class="scan-filename">📄 {h['resume_filename']}</div>
            <div class="scan-date">{h['created_at']}</div>
            <div class="scan-score" style="color:{score_color}">{int(score)}</div>
        </div>""", unsafe_allow_html=True)
