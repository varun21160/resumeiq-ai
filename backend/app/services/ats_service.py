from sqlalchemy.orm import Session

from app.models.ats_analysis import ATSAnalysis


class ATSService:
    """
    Handles database operations related to ATS analyses.
    """

    @staticmethod
    def _serialize_analyzer(value):
        """
        Convert AnalyzerResponse / Pydantic objects
        into JSON-serializable dictionaries.
        """

        if hasattr(value, "model_dump"):
            return value.model_dump()

        if hasattr(value, "dict"):
            return value.dict()

        if isinstance(value, dict):
            return {
                key: ATSService._serialize_analyzer(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                ATSService._serialize_analyzer(item)
                for item in value
            ]

        return value

    @staticmethod
    def create_analysis(
        db: Session,
        user_id: str,
        resume_id: str | None,
        job_description: str,
        report,
    ) -> ATSAnalysis:

        serialized_analysis = ATSService._serialize_analyzer(
            report.analysis
        )

        serialized_category_scores = ATSService._serialize_analyzer(
            report.category_scores
        )

        serialized_recommendations = ATSService._serialize_analyzer(
            report.recommendations
        )

        analysis = ATSAnalysis(
            user_id=user_id,
            resume_id=resume_id,
            job_description=job_description,
            overall_score=report.overall_score,
            category_scores=serialized_category_scores,
            analysis=serialized_analysis,
            recommendations=serialized_recommendations,
        )

        db.add(analysis)

        try:
            db.commit()
            db.refresh(analysis)

        except Exception:
            db.rollback()
            raise

        return analysis

    @staticmethod
    def get_analysis(
        db: Session,
        analysis_id: str,
        user_id: str,
    ) -> ATSAnalysis | None:

        return (
            db.query(ATSAnalysis)
            .filter(
                ATSAnalysis.id == analysis_id,
                ATSAnalysis.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def get_user_analyses(
        db: Session,
        user_id: str,
    ) -> list[ATSAnalysis]:

        return (
            db.query(ATSAnalysis)
            .filter(
                ATSAnalysis.user_id == user_id,
            )
            .order_by(
                ATSAnalysis.created_at.desc()
            )
            .all()
        )