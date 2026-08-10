from pprint import pprint

from app.ai.analyzers.education_analyzer import EducationAnalyzer


resume = """
Varun
B.Tech in Artificial Intelligence and Machine Learning
CGPA: 8.74
Expected Graduation Year: 2027

Python
SQL
Power BI
"""


job_description = """
We are looking for a Data Analyst with Python, SQL and Power BI.
Candidates with a degree in Computer Science, Artificial Intelligence,
Machine Learning, AIML, or related fields are preferred.
"""


result = EducationAnalyzer.analyze(
    resume,
    job_description,
)

pprint(result.model_dump())