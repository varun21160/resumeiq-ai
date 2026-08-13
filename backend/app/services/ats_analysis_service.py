from typing import Any, Dict

from sqlalchemy.orm import Session

from app.models.ats_analysis import ATSAnalysis


class ATSAnalysisService:

    @staticmethod
    def create_analysis(
        db: Session,
        user_id: str,
        resume_id: str,
        job_description: str,
        report: Dict[str, Any],
    ) -> ATSAnalysis:

        analysis = ATSAnalysis(
            user_id=user_id,
            resume_id=resume_id,
            job_description=job_description,
            overall_score=report["overall_score"],
            category_scores=report["category_scores"],
            analysis=report["analysis"],
            recommendations=report.get(
                "recommendations",
                [],
            ),
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis

    @staticmethod
    def get_analyses(
        db: Session,
        user_id: str,
    ):
        return (
            db.query(ATSAnalysis)
            .filter(
                ATSAnalysis.user_id == user_id
            )
            .order_by(
                ATSAnalysis.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_analysis(
        db: Session,
        analysis_id: str,
        user_id: str,
    ):
        return (
            db.query(ATSAnalysis)
            .filter(
                ATSAnalysis.id == analysis_id,
                ATSAnalysis.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def delete_analysis(
        db: Session,
        analysis: ATSAnalysis,
    ) -> None:

        db.delete(analysis)
        db.commit()

    @staticmethod
    def to_response(
        analysis: ATSAnalysis,
    ) -> dict:

        return {
            "id": analysis.id,
            "resume_id": analysis.resume_id,
            "job_description": analysis.job_description,
            "overall_score": analysis.overall_score,
            "category_scores": analysis.category_scores,
            "analysis": analysis.analysis,
            "recommendations": analysis.recommendations,
            "created_at": analysis.created_at,
        }