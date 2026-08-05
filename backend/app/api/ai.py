from fastapi import APIRouter

from app.schemas.ai import (
    ResumeReviewRequest,
    ResumeReviewResponse,
    ResumeTailorRequest,
    ResumeTailorResponse,
    CoverLetterRequest,
    CoverLetterResponse,
    InterviewRequest,
    InterviewResponse,
)
from app.services.ai_service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/review",
    response_model=ResumeReviewResponse,
)
def review_resume(request: ResumeReviewRequest):

    review = AIService.review_resume(
        request.resume_text
    )

    return ResumeReviewResponse(
        review=review
    )


@router.post(
    "/tailor",
    response_model=ResumeTailorResponse,
)
def tailor_resume(request: ResumeTailorRequest):

    result = AIService.tailor_resume(
        request.resume_text,
        request.job_description,
    )

    return ResumeTailorResponse(
        tailored_resume=result
    )


@router.post(
    "/cover-letter",
    response_model=CoverLetterResponse,
)
def cover_letter(request: CoverLetterRequest):

    result = AIService.generate_cover_letter(
        request.resume_text,
        request.company,
        request.job_title,
        request.job_description,
    )

    return CoverLetterResponse(
        cover_letter=result
    )


@router.post(
    "/interview",
    response_model=InterviewResponse,
)
def interview_questions(request: InterviewRequest):

    result = AIService.generate_interview_questions(
        request.resume_text,
        request.job_description,
    )

    return InterviewResponse(
        interview_questions=result
    )