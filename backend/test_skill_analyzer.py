from app.ai.analyzers.skill_analyzer import SkillAnalyzer

resume = """
Python
SQL
Power BI
Docker
AWS
FastAPI
Git
"""

jd = """
Python
SQL
Power BI
Docker
"""

result = SkillAnalyzer.analyze(
    resume,
    jd,
)

from pprint import pprint

pprint(result)