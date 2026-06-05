# 🎯 ATS Resume Scorer

A full-stack web app that scores how well your resume matches a job description and returns actionable, AI-generated feedback. Built with Streamlit and powered by Groq's Llama 3.3 70B.

**Live demo → [https://ats-scorer-2cks.onrender.com](https://ats-scorer-2cks.onrender.com)**

---

## What it does

1. Register an account and log in securely
2. Upload your resume (PDF or DOCX) and paste a job description
3. Get an ATS score out of 100, matching skills, missing keywords, and 3 specific suggestions
4. Every scan is saved to your personal dashboard — track how your score improves over time

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (custom dark UI with CSS animations) |
| LLM | Groq API — `llama-3.3-70b-versatile` |
| Resume parsing | PyPDF2, python-docx |
| Auth | bcrypt password hashing, Streamlit session state |
| Database | PostgreSQL (Render) with SQLite fallback for local dev |
| ORM | SQLAlchemy |
| Charts | Plotly |
| Deployment | Render (web service + managed PostgreSQL) |

---

## Project structure

ATS_SCORER/
├── app.py                  ← Streamlit entry point, auth gate, landing page
├── pages/
│   ├── 1_Scorer.py         ← Resume upload + analysis page
│   └── 2_Dashboard.py      ← Score history and skill gap tracker
├── backend/
│   ├── auth.py             ← Login/register UI, password hashing
│   ├── database.py         ← SQLAlchemy models, init_db, save_result, get_history
│   ├── resume_parser.py    ← Extracts text from PDF and DOCX
│   └── scorer.py           ← Groq API call, returns structured JSON
├── .env.example            ← Environment variable template (no real keys)
├── requirements.txt
└── README.md
---

## Local setup

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/Bhumi-dubey-16/ATS_SCORER
cd ATS_SCORER
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your real values:
### 4. Run the app

```bash
streamlit run app.py
```

App opens at `http://localhost:8501`.  
If `DATABASE_URL` is not set, a local `ats_scorer.db` SQLite file is created automatically — no setup needed.

---

## Deployment (Render)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → **New → PostgreSQL** → create free database → copy Internal Database URL
3. **New → Web Service** → connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Add environment variables in Render dashboard:

| Key | Value |
|---|---|
| `GROQ_API_KEY` | Your key from console.groq.com |
| `DATABASE_URL` | Internal PostgreSQL URL from Render |

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | From [console.groq.com](https://console.groq.com) |
| `DATABASE_URL` | No | PostgreSQL URL. Falls back to SQLite locally if not set |

---

