from pathlib import Path

from app.services.docx_generator import DOCXResumeGenerator


# ======================================================
# TEST RESUME DATA
# ======================================================

test_resume = {
    "name": "Varun NagaSai Mamidipaka",
    "email": "varunnagasaimamidipaka@gmail.com",
    "phone": "8340067180",
    "location": "Guntur, Andhra Pradesh, India",

    "target_role": "Data Analyst",

    "summary": (
        "Data Analyst proficient in Python, SQL, Excel, and Power BI "
        "with experience in analyzing business data, creating dashboards, "
        "and generating actionable insights."
    ),

    "skills": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Pandas",
        "Data Analysis",
        "Data Cleaning",
        "Data Visualization",
        "DAX",
        "Power Query",
    ],

    "experience": [
        {
            "company": "Apex Planet Software Pvt. Ltd.",
            "role": "Data Analytics Intern",
            "duration": "Remote",
            "bullets": [
                "Developed Power BI dashboards and reporting solutions.",
                "Performed SQL querying, data extraction, and analysis.",
                "Generated KPI-driven insights for business reporting.",
            ],
        },
        {
            "company": "Deloitte Australia (Forage)",
            "role": "Data Analytics Virtual Experience",
            "duration": "2026",
            "bullets": [
                "Analyzed business datasets to generate actionable insights.",
                "Used Excel for data analysis and classification.",
                "Built interactive Tableau dashboards for data visualization.",
            ],
        },
    ],

    "projects": [
        {
            "name": "SaaS Subscription Churn & Revenue Analytics",
            "description": (
                "Analyzed customer subscription data to identify "
                "churn trends and revenue patterns."
            ),
            "technologies": [
                "Python",
                "SQL",
                "Power BI",
            ],
            "bullets": [
                "Analyzed 10K+ customer subscription records using SQL and Python.",
                "Performed data validation and exploratory data analysis.",
                "Developed Power BI dashboards with 12+ business KPIs.",
            ],
        },
        {
            "name": "HR Analytics: Employee Attrition & Performance Analysis",
            "description": (
                "Analyzed HR records to identify attrition factors "
                "and workforce trends."
            ),
            "technologies": [
                "Python",
                "SQL",
                "Power BI",
            ],
            "bullets": [
                "Processed and analyzed 8K+ HR records.",
                "Applied statistical analysis across employee metrics.",
                "Developed Power BI dashboards with department-wise KPIs.",
            ],
        },
        {
            "name": "Sales & Business Insights Dashboard",
            "description": (
                "Designed Power BI dashboards to analyze sales "
                "transactions and customer behavior."
            ),
            "technologies": [
                "SQL",
                "Power BI",
            ],
            "bullets": [
                "Analyzed 5K+ sales transactions.",
                "Applied SQL query optimization techniques.",
                "Created reports with 15+ business KPIs.",
            ],
        },
    ],

    "education": [
        {
            "degree": (
                "B.Tech - Artificial Intelligence & Machine Learning"
            ),
            "institution": (
                "Vignan's Lara Institute of Technology & Science"
            ),
            "duration": "2023 - Present",
        }
    ],

    "certifications": [
        "HackerRank - SQL",
        "Deloitte Australia - Data Analytics Virtual Experience",
        "Geeks for Geeks - Python Course",
    ],

    "links": [
        "linkedin.com/in/varun-naga-sai-mamidipaka-79181135a",
        "github.com/varun21160",
        "varun-ns.lovable.app",
    ],
}


# ======================================================
# OUTPUT DIRECTORY
# ======================================================

output_dir = Path(
    "generated_resumes"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True,
)


# ======================================================
# 1. SINGLE COLUMN
# ======================================================

single_column_path = (
    output_dir
    / "test_resume_single_column.docx"
)

DOCXResumeGenerator.generate(
    generated_resume=test_resume,
    output_path=str(single_column_path),
    template_key="single_column",
)

print(
    "Single-column resume generated:"
)

print(
    single_column_path
)


# ======================================================
# 2. DOUBLE COLUMN
# ======================================================

mailing_address = """Flat no: G7,
Rajeev Gruha Kalpa Apartments,
YSR Colony,
Chilakaluripet - 522 616."""


double_column_path = (
    output_dir
    / "test_resume_double_column.docx"
)

DOCXResumeGenerator.generate(
    generated_resume=test_resume,
    output_path=str(double_column_path),
    template_key="double_column",
    mailing_address=mailing_address,
)

print(
    "Double-column resume generated:"
)

print(
    double_column_path
)


# ======================================================
# COMPLETE
# ======================================================

print()
print(
    "========================================"
)
print(
    "RESUME TEMPLATE TEST COMPLETED"
)
print(
    "========================================"
)