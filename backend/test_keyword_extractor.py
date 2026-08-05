from app.ai.keyword_extractor import KeywordExtractor

resume = """
Experienced Data Analyst.

Skills:

Python
SQL
Power BI
FastAPI
Docker
Git
"""

skills = KeywordExtractor.extract(resume)

print(skills)