from pprint import pprint

from app.ai.ats_report_engine import ATSReportEngine


resume = """
Varun Nagasai Mamidipaka
Data Analyst

SUMMARY
Data Analyst with 2 years of experience in Python, SQL, Power BI and FastAPI.
Experienced in data analysis, dashboard development, business analytics and
machine learning projects.

SKILLS
Python
SQL
Power BI
FastAPI
Pandas
NumPy
Machine Learning
GitHub

EXPERIENCE
Data Analyst
2 years experience
Analyzed business datasets using Python and SQL.
Developed Power BI dashboards for business reporting.
Automated data analysis workflows using Python.
Improved reporting efficiency by 30%.

PROJECTS
SaaS Subscription Analysis
Developed a subscription analytics solution using Python, SQL and Power BI.
Analyzed customer churn, MRR, ARR and subscription trends.
Improved reporting efficiency by 25%.
GitHub: https://github.com/demo/saas-analysis

Sales Analytics Dashboard
Built an interactive Power BI dashboard using Python and SQL.
Analyzed sales, profit, regional and category performance.
Reduced manual reporting time by 40%.
GitHub: https://github.com/demo/sales-dashboard

HR Analytics
Created an employee attrition analysis project using Python, SQL and Power BI.
Analyzed employee performance, attrition patterns and business KPIs.
Achieved 92% model accuracy.
GitHub: https://github.com/demo/hr-analytics

ResumeIQ AI
Developed an AI-powered resume analysis application using Python and FastAPI.
Implemented ATS scoring, skill matching and resume quality analysis.
Processed resume information and generated automated recommendations.
GitHub: https://github.com/demo/resumeiq

EDUCATION
B.Tech
Artificial Intelligence and Machine Learning
CGPA 8.74
Expected Graduation Year: 2027

CERTIFICATIONS
NPTEL Python for Data Science
HackerRank SQL
Power BI Certification

CONTACT
demo@example.com
+91 9876543210
https://linkedin.com/in/demo
https://github.com/demo
https://portfolio.com
"""


jd = """
Looking for Data Analyst

Requirements:
Python
SQL
Power BI
FastAPI
Pandas
Data Analysis
Dashboard Development
Business Analytics
Machine Learning

Education:
B.Tech in Artificial Intelligence and Machine Learning

Certifications:
NPTEL
Power BI

Preferred:
AWS
Strong analytical and problem-solving skills
Ability to communicate insights clearly
"""


report = ATSReportEngine.generate(
    resume,
    jd,
)

print("\n========== ATS REPORT ==========\n")

pprint(report.model_dump())

print("\n================================")