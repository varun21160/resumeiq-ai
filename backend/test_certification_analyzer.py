from pprint import pprint

from app.ai.analyzers.certification_analyzer import CertificationAnalyzer

resume = """
NPTEL Python for Data Science

Cisco Data Science

Power BI

Hackerrank SQL

Coursera Machine Learning
"""

jd = """
Looking for Python, SQL, Power BI,
NPTEL, Coursera certifications.
"""

result = CertificationAnalyzer.analyze(
    resume,
    jd,
)

pprint(result.model_dump())