import streamlit as st
import bcrypt
from backend.database import get_user, create_user

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def login_ui():
    if st.session_state.get("authenticated"):
        return True

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #0a0a0f; color: #e8e8f0; }
    #MainMenu, footer, header { visibility: hidden; }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .login-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 20px 20px; text-align: center; }
    .login-badge { display: inline-block; font-family: 'Syne', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: #6c63ff; border: 1px solid rgba(108,99,255,0.3); background: rgba(108,99,255,0.08); padding: 6px 18px; border-radius: 100px; margin-bottom: 24px; animation: fadeUp 0.5s ease both; }
    .login-title { font-family: 'Syne', sans-serif; font-size: 40px; font-weight: 800; color: #f0f0ff; margin-bottom: 8px; animation: fadeUp 0.5s ease 0.1s both; }
    .login-title .grad { background: linear-gradient(135deg, #6c63ff, #a78bfa, #6c63ff); background-size: 200% 200%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradientShift 4s ease infinite; }
    .login-sub { font-size: 14px; color: #4a4a60; margin-bottom: 40px; animation: fadeUp 0.5s ease 0.2s both; }
    div[data-testid="stTextInput"] input { background: #111118 !important; border: 1px solid #1e1e2e !important; border-radius: 12px !important; color: #e8e8f0 !important; font-family: 'DM Sans', sans-serif !important; font-size: 14px !important; padding: 12px 16px !important; transition: border-color 0.2s !important; }
    div[data-testid="stTextInput"] input:focus { border-color: #6c63ff !important; box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important; }
    div[data-testid="stButton"] button { background: linear-gradient(135deg, #6c63ff, #a78bfa) !important; color: white !important; border: none !important; border-radius: 12px !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; letter-spacing: 2px !important; text-transform: uppercase !important; font-size: 11px !important; padding: 14px !important; width: 100% !important; transition: all 0.3s ease !important; }
    div[data-testid="stButton"] button:hover { transform: translateY(-2px) !important; box-shadow: 0 12px 32px rgba(108,99,255,0.35) !important; }
    div[data-testid="stTabs"] [data-baseweb="tab-list"] { background: #111118 !important; border-radius: 12px !important; padding: 4px !important; border: 1px solid #1e1e2e !important; gap: 4px !important; }
    div[data-testid="stTabs"] [data-baseweb="tab"] { border-radius: 10px !important; font-family: 'Syne', sans-serif !important; font-size: 11px !important; font-weight: 700 !important; letter-spacing: 2px !important; text-transform: uppercase !important; color: #4a4a60 !important; transition: all 0.2s !important; }
    div[data-testid="stTabs"] [aria-selected="true"] { background: rgba(108,99,255,0.15) !important; color: #6c63ff !important; }
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: transparent !important; }
    div[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-wrap">
        <div class="login-badge">✦ ATS Resume Scorer</div>
        <div class="login-title">Welcome <span class="grad">Back</span></div>
        <div class="login-sub">Sign in to your account or create a new one below.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        tab_login, tab_register = st.tabs(["  Login  ", "  Register  "])

        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username", key="login_user", placeholder="your_username")
            password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Login →", key="btn_login", use_container_width=True):
                if not username or not password:
                    st.error("Please fill in both fields.")
                else:
                    user = get_user(username)
                    if user and verify_password(password, user.hashed_password):
                        st.session_state["authenticated"] = True
                        st.session_state["username"]      = user.username
                        st.session_state["name"]          = user.name
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        with tab_register:
            st.markdown("<br>", unsafe_allow_html=True)
            new_name  = st.text_input("Full Name",        key="reg_name",  placeholder="Bhumi Dubey")
            new_email = st.text_input("Email",            key="reg_email", placeholder="bhumi@email.com")
            new_user  = st.text_input("Username",         key="reg_user",  placeholder="bhumi_16")
            new_pass  = st.text_input("Password",         type="password", key="reg_pass",  placeholder="min 6 characters")
            new_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2", placeholder="repeat password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account →", key="btn_register", use_container_width=True):
                if not all([new_name, new_email, new_user, new_pass, new_pass2]):
                    st.error("Please fill in all fields.")
                elif new_pass != new_pass2:
                    st.error("Passwords do not match.")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                elif get_user(new_user):
                    st.error("Username already taken.")
                else:
                    try:
                        create_user(username=new_user, email=new_email, name=new_name, hashed_password=hash_password(new_pass))
                        st.success("Account created! Please login.")
                    except Exception as e:
                        st.error(f"Error: {e}")

    return False
