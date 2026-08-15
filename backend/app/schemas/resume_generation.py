from typing import List, Literal

from pydantic import BaseModel, Field, model_validator


class ResumeGenerationRequest(BaseModel):

    job_description: str = Field(
        ...,
        min_length=50,
        description="Target job description",
    )

    template: Literal[
        "single_column",
        "double_column",
    ] = Field(
        default="single_column",
        description="Resume layout template",
    )

    mailing_address: str | None = Field(
        default=None,
        max_length=500,
        description=(
            "Required for double-column resumes. "
            "Not used for single-column resumes."
        ),
    )

    @model_validator(mode="after")
    def validate_template_requirements(self):

        if self.template == "double_column":

            if not self.mailing_address:
                raise ValueError(
                    "Mailing address is required "
                    "for double-column resumes."
                )

            if not self.mailing_address.strip():
                raise ValueError(
                    "Mailing address cannot be empty."
                )

        return self


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
    id: str
    resume_id: str
    ats_score: int
    generated_resume: GeneratedResume
    changes: List[str] = Field(
        default_factory=list
    )