from pydantic import BaseModel


class ATSRequest(BaseModel):
    resume_id: str
    job_description: str


class ATSResponse(BaseModel):
    ats_score: int
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    job_description_skills: list[str]