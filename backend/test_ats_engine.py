from app.ai.ats_engine import ATSEngine

resume = """
Data Analyst

Skills

Python
SQL
Power BI
FastAPI
Docker
Git
"""

job_description = """
We are looking for a Data Analyst.

Required Skills

Python
SQL
Docker
AWS
Kafka
"""

result = ATSEngine.analyze(
    resume,
    job_description,
)

print(result)