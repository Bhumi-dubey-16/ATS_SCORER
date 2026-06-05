from backend.scorer import score_resume

resume = """
John Doe
Skills: Python, SQL, Data Analysis, Excel
Experience: 2 years as Business Analyst at XYZ company
Education: B.Tech Computer Science
"""

jd = """
Looking for a Data Analyst with experience in Python, SQL, 
Power BI, Tableau, and machine learning. Must have strong 
communication skills and experience with stakeholder management.
"""

result = score_resume(resume, jd)
print(result)
