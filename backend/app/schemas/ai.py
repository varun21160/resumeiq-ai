from pydantic import BaseModel


class ResumeReviewRequest(BaseModel):
    resume_text: str


class ResumeReviewResponse(BaseModel):
    review: str


class ResumeTailorRequest(BaseModel):
    resume_text: str
    job_description: str


class ResumeTailorResponse(BaseModel):
    tailored_resume: str


class CoverLetterRequest(BaseModel):
    resume_text: str
    company: str
    job_title: str
    job_description: str


class CoverLetterResponse(BaseModel):
    cover_letter: str


class InterviewRequest(BaseModel):
    resume_text: str
    job_description: str


class InterviewResponse(BaseModel):
    interview_questions: str