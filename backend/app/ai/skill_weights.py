"""
Importance of skills for ATS scoring.
Higher value = More important.
"""

SKILL_WEIGHTS = {

    # Programming
    "python": 10,
    "java": 9,
    "javascript": 8,
    "typescript": 8,

    # Databases
    "sql": 10,
    "mysql": 8,
    "postgresql": 9,
    "mongodb": 7,

    # Analytics
    "excel": 7,
    "power bi": 9,
    "tableau": 8,

    # ML
    "machine learning": 9,
    "tensorflow": 9,
    "pytorch": 9,
    "scikit-learn": 8,

    # Backend
    "fastapi": 8,
    "django": 8,
    "flask": 7,

    # Cloud
    "aws": 10,
    "azure": 9,
    "gcp": 9,

    # DevOps
    "docker": 8,
    "kubernetes": 9,
    "git": 3,
    "github": 2,

    # Big Data
    "spark": 8,
    "pyspark": 9,
    "hadoop": 7,
    "kafka": 8,
}