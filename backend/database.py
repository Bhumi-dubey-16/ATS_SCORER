from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "ats_scores.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

Base = declarative_base()

# ------------------------------------------------------------------
# Table definition — one row = one resume scan
# ------------------------------------------------------------------
class ScanResult(Base):
    __tablename__ = "scan_results"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    resume_filename = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=False)
    score           = Column(Float, nullable=False)
    matching_skills = Column(Text)   # stored as JSON string
    missing_keywords= Column(Text)   # stored as JSON string
    suggestions     = Column(Text)   # stored as JSON string
    summary         = Column(Text)
    created_at      = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ScanResult id={self.id} file={self.resume_filename} score={self.score}>"


# ------------------------------------------------------------------
# Call once at app startup — creates the table if it doesn't exist
# ------------------------------------------------------------------
def init_db():
    Base.metadata.create_all(engine)


# ------------------------------------------------------------------
# Save a scan result to the database
# result_dict is the parsed JSON from scorer.py
# ------------------------------------------------------------------
def save_result(resume_filename, job_description, result_dict):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        record = ScanResult(
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
        return record.id   # return the new row's ID
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# ------------------------------------------------------------------
# Fetch last N scans for the dashboard history table
# ------------------------------------------------------------------
def get_history(limit=10):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        rows = (
            session.query(ScanResult)
            .order_by(ScanResult.created_at.desc())
            .limit(limit)
            .all()
        )

        # Convert to plain dicts so Streamlit can use them easily
        results = []
        for row in rows:
            results.append({
                "id"              : row.id,
                "resume_filename" : row.resume_filename,
                "score"           : row.score,
                "matching_skills" : json.loads(row.matching_skills or "[]"),
                "missing_keywords": json.loads(row.missing_keywords or "[]"),
                "suggestions"     : json.loads(row.suggestions or "[]"),
                "summary"         : row.summary,
                "created_at"      : row.created_at.strftime("%Y-%m-%d %H:%M")
            })
        return results
    finally:
        session.close()
