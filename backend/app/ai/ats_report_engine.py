from app.ai.analyzers.certification_analyzer import CertificationAnalyzer
from app.ai.analyzers.education_analyzer import EducationAnalyzer
from app.ai.analyzers.experience_analyzer import ExperienceAnalyzer
from app.ai.analyzers.project_analyzer import ProjectAnalyzer
from app.ai.analyzers.skill_analyzer import SkillAnalyzer
from app.ai.overall_ats_scorer import OverallATSScorer
from app.schemas.ats_report import ATSReport

class ATSReportEngine:
    """
    Runs all analyzers and generates
    a complete ATS report.
    """

    @classmethod
    def generate(
        cls,
        resume_text: str,
        job_description: str,
    ):

        skill = SkillAnalyzer.analyze(
            resume_text,
            job_description,
        )

        experience = ExperienceAnalyzer.analyze(
            resume_text,
            job_description,
        )

        project = ProjectAnalyzer.analyze(
            resume_text,
            job_description,
        )

        education = EducationAnalyzer.analyze(
            resume_text,
            job_description,
        )

        certification = CertificationAnalyzer.analyze(
            resume_text,
            job_description,
        )

        scores = {
            "skills": skill.score,
            "experience": experience.score,
            "projects": project.score,
            "education": education.score,
            "certifications": certification.score,
        }

        overall_score = OverallATSScorer.calculate(scores)

        recommendations = []

        recommendations.extend(skill.recommendations)
        recommendations.extend(experience.recommendations)
        recommendations.extend(project.recommendations)
        recommendations.extend(education.recommendations)
        recommendations.extend(certification.recommendations)

        return ATSReport(
    overall_score=overall_score,
    category_scores=scores,
    analysis={
        "skills": skill,
        "experience": experience,
        "projects": project,
        "education": education,
        "certifications": certification,
    },
    recommendations=sorted(set(recommendations)),
)