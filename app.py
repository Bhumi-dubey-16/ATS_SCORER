import streamlit as st

st.set_page_config(
    page_title="ATS Resume Scorer",
    page_icon="📄",
    layout="centered"
)

scorer = st.Page("pages/1_Scorer.py", title="Scorer", icon="📄")
dashboard = st.Page("pages/2_Dashboard.py", title="Dashboard", icon="📊")

pg = st.navigation([scorer, dashboard])

with st.sidebar:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@800&display=swap');
    </style>
    <div style="padding: 8px 8px 24px; border-bottom: 1px solid #1a1a2a; margin-bottom: 8px;">
        <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:800; color:#f0f0ff;">
            ATS <span style="background:linear-gradient(135deg,#6c63ff,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Scorer</span>
        </div>
        <div style="font-size:10px; letter-spacing:2px; color:#4a4a60; margin-top:4px; text-transform:uppercase;">Career Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

pg.run()
