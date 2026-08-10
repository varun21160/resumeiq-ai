from typing import Dict, List

from app.ai.analyzers.certification_analyzer import CertificationAnalyzer
from app.ai.analyzers.education_analyzer import EducationAnalyzer
from app.ai.analyzers.experience_analyzer import ExperienceAnalyzer
from app.ai.analyzers.project_analyzer import ProjectAnalyzer
from app.ai.analyzers.skill_analyzer import SkillAnalyzer
from app.ai.overall_ats_scorer import OverallATSScorer
from app.ai.semantic_analyzer import SemanticAnalyzer
from app.schemas.ats_report import ATSReport


class ATSReportEngine:
    """
    Runs all deterministic analyzers and the semantic analyzer
    to generate a complete ATS report.

    Deterministic analyzers are responsible for numerical scoring.

    SemanticAnalyzer provides contextual AI analysis such as:
    - Strong matches
    - Partial matches
    - Missing requirements
    - Critical missing requirements
    - Preferred missing requirements
    - Experience relevance
    - Project relevance
    - Education relevance
    - AI recommendations
    """

    @classmethod
    def generate(
        cls,
        resume_text: str,
        job_description: str,
    ) -> ATSReport:
        """
        Generate the complete ATS report.
        """

        # --------------------------------------------------
        # Deterministic analysis
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Category scores
        # --------------------------------------------------

        scores = {
            "skills": skill.score,
            "experience": experience.score,
            "projects": project.score,
            "education": education.score,
            "certifications": certification.score,
        }

        # --------------------------------------------------
        # Deterministic overall ATS score
        #
        # Gemini does NOT modify this score.
        # --------------------------------------------------

        overall_score = OverallATSScorer.calculate(
            scores
        )

        # --------------------------------------------------
        # Semantic AI analysis
        # --------------------------------------------------

        semantic = SemanticAnalyzer.analyze(
            resume_text,
            job_description,
        )

        # --------------------------------------------------
        # Combine deterministic recommendations
        # --------------------------------------------------

        recommendations: List[str] = []

        recommendations.extend(
            skill.recommendations
        )

        recommendations.extend(
            experience.recommendations
        )

        recommendations.extend(
            project.recommendations
        )

        recommendations.extend(
            education.recommendations
        )

        recommendations.extend(
            certification.recommendations
        )

        # --------------------------------------------------
        # Add AI recommendations
        # --------------------------------------------------

        recommendations.extend(
            semantic.get(
                "recommendations",
                [],
            )
        )

        # --------------------------------------------------
        # Remove duplicate recommendations
        # --------------------------------------------------

        recommendations = sorted(
            set(
                recommendation.strip()
                for recommendation in recommendations
                if recommendation
                and recommendation.strip()
            )
        )

        # --------------------------------------------------
        # Final report
        # --------------------------------------------------

        return ATSReport(
            overall_score=overall_score,

            category_scores=scores,

            analysis={
                "skills": skill,
                "experience": experience,
                "projects": project,
                "education": education,
                "certifications": certification,

                "semantic": semantic,
            },

            recommendations=recommendations,
        )