from pprint import pprint

from app.ai.validators.resume_truthfulness_validator import (
    ResumeTruthfulnessValidator,
)


original_resume = """
Varun NagaSai Mamidipaka

Skills:
Python, SQL, Excel, Power BI, Pandas, NumPy, GitHub

Projects:
SaaS Subscription Churn & Revenue Analytics
HR Analytics using Python and SQL

Certifications:
NPTEL Python for Data Science
HackerRank SQL
"""


generated_resume = {
    "skills": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "DAX",
        "Power Query",
        "AWS",
    ]
}


result = ResumeTruthfulnessValidator.validate(
    original_resume_text=original_resume,
    generated_resume=generated_resume,
)

pprint(result)