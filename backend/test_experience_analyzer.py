from pprint import pprint

from app.ai.analyzers.experience_analyzer import ExperienceAnalyzer

resume = """
Data Analyst

2 years experience

Python
SQL
Power BI

Worked on sales dashboards.
"""

jd = """
Looking for a Data Analyst with Python and SQL.
"""

result = ExperienceAnalyzer.analyze(
    resume,
    jd,
)

pprint(result)