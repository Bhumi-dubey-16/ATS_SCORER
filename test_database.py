from backend.database import init_db, save_result, get_history

# 1. Create the table
init_db()
print("✅ Database initialized")

# 2. Save a fake scan result
fake_result = {
    "score": 72,
    "matching_skills": ["Python", "SQL"],
    "missing_keywords": ["Power BI", "Tableau"],
    "suggestions": ["Add Power BI projects", "Learn Tableau basics", "Mention stakeholder experience"],
    "summary": "Good technical foundation. Needs more BI tool experience."
}

record_id = save_result("john_doe_resume.pdf", "Data Analyst role at XYZ", fake_result)
print(f"✅ Saved result with ID: {record_id}")

# 3. Fetch history
history = get_history()
print(f"✅ Found {len(history)} record(s) in history")
print(history[0])
