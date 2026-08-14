from typing import List

from pydantic import BaseModel, Field


class ResumeGenerationRequest(BaseModel):
    job_description: str = Field(
        ...,
        min_length=50,
        description="Target job description",
    )


class GeneratedExperience(BaseModel):
    company: str
    role: str
    duration: str
    bullets: List[str]


class GeneratedProject(BaseModel):
    name: str
    description: str
    technologies: List[str]
    bullets: List[str]


class GeneratedEducation(BaseModel):
    degree: str
    institution: str
    duration: str


class GeneratedResume(BaseModel):
    name: str
    email: str
    phone: str
    location: str

    summary: str

    skills: List[str]

    experience: List[GeneratedExperience]

    projects: List[GeneratedProject]

    education: List[GeneratedEducation]

    certifications: List[str]

    links: List[str] = Field(
        default_factory=list
    )


class ResumeGenerationResponse(BaseModel):
    resume_id: str
    ats_score: int
    generated_resume: GeneratedResume
    changes: List[str] = Field(
        default_factory=list
    )