from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Fix Render's postgres:// prefix
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fall back to SQLite for local dev if DATABASE_URL not set
if not DATABASE_URL:
    BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, '..', 'ats_scorer.db')}"
    print(f"[DB] No DATABASE_URL found — using SQLite at {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    # SQLite needs this arg; PostgreSQL ignores it safely
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    username        = Column(String(100), unique=True, nullable=False)
    email           = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name            = Column(String(255), nullable=False)
    created_at      = Column(DateTime, default=datetime.utcnow)


class ScanResult(Base):
    __tablename__ = "scan_results"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    user_id          = Column(String(100), nullable=False)
    resume_filename  = Column(String(255), nullable=False)
    job_description  = Column(Text, nullable=False)
    score            = Column(Float, nullable=False)
    matching_skills  = Column(Text)
    missing_keywords = Column(Text)
    suggestions      = Column(Text)
    summary          = Column(Text)
    created_at       = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(engine)


def save_result(username, resume_filename, job_description, result_dict):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        record = ScanResult(
            user_id          = username,
            resume_filename  = resume_filename,
            job_description  = job_description,
            score            = result_dict.get("score", 0),
            matching_skills  = json.dumps(result_dict.get("matching_skills", [])),
            missing_keywords = json.dumps(result_dict.get("missing_keywords", [])),
            suggestions      = json.dumps(result_dict.get("suggestions", [])),
            summary          = result_dict.get("summary", "")
        )
        session.add(record)
        session.commit()
        return record.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_history(username, limit=10):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        rows = (
            session.query(ScanResult)
            .filter(ScanResult.user_id == username)
            .order_by(ScanResult.created_at.desc())
            .limit(limit)
            .all()
        )
        results = []
        for row in rows:
            results.append({
                "id"              : row.id,
                "resume_filename" : row.resume_filename,
                "score"           : row.score,
                "matching_skills" : json.loads(row.matching_skills  or "[]"),
                "missing_keywords": json.loads(row.missing_keywords or "[]"),
                "suggestions"     : json.loads(row.suggestions      or "[]"),
                "summary"         : row.summary,
                "created_at"      : row.created_at.strftime("%Y-%m-%d %H:%M")
            })
        return results
    finally:
        session.close()


def get_user(username):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        return session.query(User).filter(User.username == username).first()
    finally:
        session.close()


def create_user(username, email, name, hashed_password):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user = User(
            username        = username,
            email           = email,
            name            = name,
            hashed_password = hashed_password
        )
        session.add(user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
