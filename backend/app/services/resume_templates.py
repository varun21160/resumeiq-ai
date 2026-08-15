from dataclasses import dataclass
from typing import Literal


TemplateType = Literal[
    "single_column",
    "double_column",
]


@dataclass(frozen=True)
class ResumeTemplate:

    key: str
    name: str
    description: str
    columns: int
    ats_priority: str


SINGLE_COLUMN = ResumeTemplate(
    key="single_column",
    name="ATS Single Column",
    description=(
        "Clean single-column resume designed "
        "for strong ATS parsing compatibility."
    ),
    columns=1,
    ats_priority="Maximum",
)


DOUBLE_COLUMN = ResumeTemplate(
    key="double_column",
    name="Professional Double Column",
    description=(
        "Professional two-column resume inspired "
        "by the supplied reference layout."
    ),
    columns=2,
    ats_priority="High",
)


RESUME_TEMPLATES = {
    SINGLE_COLUMN.key: SINGLE_COLUMN,
    DOUBLE_COLUMN.key: DOUBLE_COLUMN,
}


def get_template(
    template_key: str,
) -> ResumeTemplate:

    template = RESUME_TEMPLATES.get(
        template_key
    )

    if template is None:
        raise ValueError(
            f"Unknown resume template: {template_key}"
        )

    return template


def get_all_templates() -> list[ResumeTemplate]:

    return list(
        RESUME_TEMPLATES.values()
    )