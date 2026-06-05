# 🎯 ATS Resume Scorer

A full-stack web app that scores how well your resume matches a job description and returns actionable, AI-generated feedback. Built with Streamlit and powered by Groq's Llama 3.3 70B.

**Live demo → [https://ats-scorer-2cks.onrender.com](https://ats-scorer-2cks.onrender.com)**

<div align="center">

# ATS Resume Scorer

**AI-powered resume analysis. Know exactly why you're not getting callbacks.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20App-4F46E5?style=for-the-badge)](https://ats-scorer-2cks.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-F55036?style=for-the-badge)](https://groq.com)

</div>

---

## Overview

Most resume screeners fail candidates before a human ever reads their application. ATS Resume Scorer gives job seekers the same lens recruiters use — upload your resume, paste a job description, and get a structured match analysis in seconds.

Unlike keyword-matching tools, this app uses a 70B parameter LLM to understand semantic relevance — not just whether the word "Python" appears, but whether your experience actually aligns with what the role demands.

---

## Features

- **Secure authentication** — register and log in with bcrypt-hashed credentials
- **Resume parsing** — supports PDF and DOCX formats
- **AI-powered scoring** — match score out of 100 with structured JSON output from Llama 3.3 70B via Groq
- **Gap analysis** — matching skills, missing keywords, and 3 concrete improvement suggestions per scan
- **Personal dashboard** — every scan is persisted; track score progression and identify recurring skill gaps across all your applications
- **Zero-config local dev** — falls back to SQLite automatically if no database URL is set

---

## Tech stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | UI, multipage routing, session state |
| LLM | Groq API — `llama-3.3-70b-versatile` | Resume-JD semantic analysis |
| Resume parsing | PyPDF2, python-docx | Text extraction from PDF and DOCX |
| Auth | bcrypt + Streamlit session state | Password hashing, login flow |
| Database | PostgreSQL (prod) / SQLite (local) | Scan history persistence |
| ORM | SQLAlchemy | Database models and queries |
| Charts | Plotly | Score progression, skill gap visualization |
| Deployment | Render | Web service + managed PostgreSQL |

---

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Streamlit  │────▶│ resume_parser│────▶│   Groq API      │
│   Frontend   │     │  (PDF/DOCX)  │     │ llama-3.3-70b   │
└─────────────┘     └──────────────┘     └────────┬────────┘
       │                                           │
       │              ┌────────────────────────────▼────────┐
       │              │         Structured JSON Response      │
       │              │  score · matching_skills · missing   │
       │              │  keywords · suggestions · summary    │
       │              └────────────────────────────┬────────┘
       │                                           │
       ▼                                           ▼
┌─────────────┐                         ┌─────────────────┐
│  Auth Layer  │                         │   PostgreSQL /  │
│   bcrypt     │                         │    SQLite DB    │
└─────────────┘                         └─────────────────┘
```

---

## Project structure

```
ATS_SCORER/
├── app.py                  # Entry point — auth gate and landing page
├── pages/
│   ├── 1_Scorer.py         # Resume upload, JD input, analysis results
│   └── 2_Dashboard.py      # Score history, progression charts, skill gap tracker
├── backend/
│   ├── auth.py             # Login/register UI, bcrypt password hashing
│   ├── database.py         # SQLAlchemy models, init_db, save_result, get_history
│   ├── resume_parser.py    # PDF and DOCX text extraction
│   └── scorer.py           # Groq API integration, prompt engineering, JSON parsing
├── .env.example            # Environment variable template
├── requirements.txt
└── README.md
```

---

## Getting started

### Prerequisites

- Python 3.11+
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repository

```bash
git clone https://github.com/Bhumi-dubey-16/ATS_SCORER
cd ATS_SCORER
```

### 2. Create a virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and set your values:

```env
GROQ_API_KEY=your_key_here
DATABASE_URL=                   # Optional — leave blank to use local SQLite
```

> **Note:** If `DATABASE_URL` is not set, the app automatically creates a local `ats_scorer.db` SQLite file. No database setup required for local development.

### 5. Run the app

```bash
streamlit run app.py
```

Navigate to [http://localhost:8501](http://localhost:8501).

---

## Deployment

This app is configured for one-click deployment on [Render](https://render.com).

### Steps

1. Push your repository to GitHub
2. On Render: **New → PostgreSQL** → create a free database → copy the **Internal Database URL**
3. **New → Web Service** → connect your GitHub repository
4. Configure the service:

| Setting | Value |
|---|---|
| Build command | `pip install -r requirements.txt` |
| Start command | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` |

5. Set environment variables:

| Key | Value |
|---|---|
| `GROQ_API_KEY` | Your key from [console.groq.com](https://console.groq.com) |
| `DATABASE_URL` | Internal PostgreSQL URL from Render |

---

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | Yes | — | API key from [console.groq.com](https://console.groq.com) |
| `DATABASE_URL` | No | SQLite fallback | PostgreSQL connection string for production |

---

## License

MIT