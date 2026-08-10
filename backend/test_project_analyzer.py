from pprint import pprint

from app.ai.analyzers.project_analyzer import ProjectAnalyzer


resume = """
PROJECTS

SaaS Subscription Churn Analysis
Developed a churn analysis solution using Python, SQL and Power BI.
Analyzed 10,000 customer records and achieved 92% prediction accuracy.
GitHub: github.com/example/churn-analysis

HR Analytics Dashboard
Built an HR analytics dashboard using Power BI, Python and SQL.
Reduced manual reporting time by 30%.

EDUCATION

B.Tech in Artificial Intelligence and Machine Learning
CGPA: 8.7
"""


job_description = """
We are looking for a Data Analyst with strong Python,
SQL and Power BI skills.

Experience with data analytics, dashboards and
machine learning is preferred.
"""


result = ProjectAnalyzer.analyze(
    resume,
    job_description,
)

pprint(result.model_dump())