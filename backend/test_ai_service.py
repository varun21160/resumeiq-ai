from app.services.ai_service import AIService

resume = """
Data Analyst

Skills:
Python
SQL
Power BI
Excel

Projects:
Sales Dashboard
HR Analytics
"""

response = AIService.review_resume(resume)

print(response)