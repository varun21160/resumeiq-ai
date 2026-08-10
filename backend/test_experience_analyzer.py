from pprint import pprint

from app.ai.analyzers.experience_analyzer import ExperienceAnalyzer


resume = """
Data Analytics Intern

Worked on data analysis using Python, SQL and Power BI.
Built dashboards and analyzed business datasets.

Machine Learning Intern

Developed machine learning models using Python.

B.Tech in Artificial Intelligence and Machine Learning.
"""


job_description = """
We are looking for a Data Analyst.

The candidate should have experience with Python,
SQL and Power BI.

Experience with data analytics and machine learning
is preferred.
"""


result = ExperienceAnalyzer.analyze(
    resume,
    job_description,
)

pprint(result.model_dump())