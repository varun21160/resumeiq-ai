from pprint import pprint

from app.ai.semantic_analyzer import SemanticAnalyzer


resume_text = """
Varun is a B.Tech student specializing in Artificial Intelligence
and Machine Learning with a CGPA of 8.74.

Skills:
Python, SQL, Power BI, FastAPI, Git.

Experience:
Data Analyst with experience in SQL, Python and Power BI.

Projects:
Built a sales analytics dashboard using Python, SQL and Power BI.
Developed a FastAPI-based resume analysis application.
Created machine learning projects involving data analysis.

Certifications:
NPTEL Python for Data Science.
HackerRank SQL certification.
"""


job_description = """
We are looking for a Data Analyst.

Requirements:
- Strong Python and SQL skills
- Experience with Power BI and dashboard development
- Data analysis and visualization experience
- Strong analytical and problem-solving skills
- Experience with AWS is preferred
- Experience working with business datasets
- Ability to communicate insights clearly
"""


result = SemanticAnalyzer.analyze(
    resume_text=resume_text,
    job_description=job_description,
)

pprint(result)