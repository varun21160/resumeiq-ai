from app.ai.analyzers.certification_analyzer import CertificationAnalyzer
from app.ai.analyzers.education_analyzer import EducationAnalyzer
from app.ai.analyzers.experience_analyzer import ExperienceAnalyzer
from app.ai.analyzers.project_analyzer import ProjectAnalyzer
from app.ai.analyzers.skill_analyzer import SkillAnalyzer
from app.ai.analyzers.resume_quality_analyzer import ResumeQualityAnalyzer

from app.ai.overall_ats_scorer import OverallATSScorer
from app.resume.section_detector import SectionDetector
from app.schemas.ats_report import ATSReport


class ATSReportEngine:
    """
    Runs all deterministic analyzers and generates
    the complete ATS report.

    Section-based analyzers receive only their relevant
    resume section wherever possible.
    """

    @classmethod
    def generate(
        cls,
        resume_text: str,
        job_description: str,
    ):
        # --------------------------------------------------
        # Validate input
        # --------------------------------------------------

        if not resume_text or not resume_text.strip():
            raise ValueError(
                "Resume text cannot be empty."
            )

        if not job_description or not job_description.strip():
            raise ValueError(
                "Job description cannot be empty."
            )

        # --------------------------------------------------
        # Detect resume sections
        # --------------------------------------------------

        sections = SectionDetector.detect(
            resume_text
        )

        # --------------------------------------------------
        # Get individual sections
        # --------------------------------------------------

        certifications_text = sections.get(
            "certifications",
            "",
        )

        education_text = sections.get(
            "education",
            "",
        )

        experience_text = sections.get(
            "experience",
            "",
        )

        internships_text = sections.get(
            "internships",
            "",
        )

        projects_text = sections.get(
            "projects",
            "",
        )

        # --------------------------------------------------
        # Skills
        #
        # SkillAnalyzer currently works with the complete
        # resume because skills may appear in multiple
        # sections.
        # --------------------------------------------------

        skill = SkillAnalyzer.analyze(
            resume_text,
            job_description,
        )

        # --------------------------------------------------
        # Experience
        #
        # ExperienceAnalyzer needs to detect professional
        # experience and internships, so keep the complete
        # resume as input.
        # --------------------------------------------------

        experience = ExperienceAnalyzer.analyze(
            resume_text,
            job_description,
        )

        # --------------------------------------------------
        # Projects
        #
        # ProjectAnalyzer already contains its own project
        # section extraction logic.
        # Therefore keep passing the complete resume.
        # --------------------------------------------------

        project = ProjectAnalyzer.analyze(
            resume_text,
            job_description,
        )

        # --------------------------------------------------
        # Education
        #
        # EducationAnalyzer can safely work with the complete
        # resume because it extracts education information.
        # --------------------------------------------------

        education = EducationAnalyzer.analyze(
            resume_text,
            job_description,
        )

        # --------------------------------------------------
        # Certifications
        #
        # IMPORTANT:
        # Only pass the certification section.
        #
        # This prevents CONTACT, phone numbers, email,
        # LinkedIn, etc. from being detected as
        # certifications.
        # --------------------------------------------------

        certification_source = (
            certifications_text
            if certifications_text.strip()
            else resume_text
        )
        print("\n========== CERTIFICATION SECTION DEBUG ==========")
        print(certification_source)
        print("================================================")

        certification = CertificationAnalyzer.analyze(
            certification_source,
            job_description,
        )

        # --------------------------------------------------
        # Resume Quality
        #
        # ResumeQualityAnalyzer must receive the complete
        # resume because it evaluates:
        # - sections
        # - word count
        # - contact information
        # - bullets
        # - action verbs
        # - measurable results
        # --------------------------------------------------

        resume_quality = ResumeQualityAnalyzer.analyze(
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
            "resume_quality": resume_quality.score,
        }

        # --------------------------------------------------
        # Overall ATS score
        # --------------------------------------------------

        overall_score = OverallATSScorer.calculate(
            scores
        )

        # --------------------------------------------------
        # Combine recommendations
        # --------------------------------------------------

        recommendations = []

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

        recommendations.extend(
            resume_quality.recommendations
        )

        # Remove duplicates and sort
        recommendations = sorted(
            set(recommendations)
        )

        # --------------------------------------------------
        # Final ATS report
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
                "resume_quality": resume_quality,
            },
            recommendations=recommendations,
        )