from pprint import pprint

from app.ai.ats_report_engine import ATSReportEngine

resume = """
Data Analyst

2 years experience

Projects

Developed ResumeIQ AI

Python
SQL
Power BI
FastAPI

B.Tech

Artificial Intelligence and Machine Learning

CGPA 8.74

NPTEL Python

Hackerrank SQL

https://github.com/demo

https://portfolio.com
"""

jd = """
Looking for Data Analyst

Python

SQL

Power BI

FastAPI

B.Tech AIML

NPTEL

Power BI
"""

report = ATSReportEngine.generate(
    resume,
    jd,
)

from pprint import pprint
pprint(report.model_dump())