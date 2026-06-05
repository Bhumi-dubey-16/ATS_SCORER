import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def score_resume(resume_text, job_description):
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) analyzer.
    
    Analyze this resume against the job description and respond ONLY in this exact JSON format:
    {{
        "score": <number 0-100>,
        "matching_skills": [<list of skills found in both resume and JD>],
        "missing_keywords": [<list of important keywords in JD but missing from resume>],
        "suggestions": [<exactly 3 specific improvement suggestions>],
        "summary": "<2 sentence overall assessment>"
    }}

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    Respond with JSON only. No explanation, no markdown, no extra text.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        timeout=30
    )

    return response.choices[0].message.content
