from pprint import pprint

from app.ai.analyzers.project_analyzer import ProjectAnalyzer

resume = """
Projects

Developed ResumeIQ AI

Built HR Analytics Dashboard

Python
SQL
Power BI
FastAPI

https://github.com/user/project

https://portfolio.com
"""

jd = """
Python
SQL
Power BI
FastAPI
"""

result = ProjectAnalyzer.analyze(
    resume,
    jd,
)

pprint(result)