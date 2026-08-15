from pathlib import Path
from typing import Dict

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from app.services.resume_templates import get_template


class DOCXResumeGenerator:
    """
    Generates ATS-friendly DOCX resumes.

    Supported templates:
        - ats_classic
        - corporate_ats
    """

    @staticmethod
    def generate(
        generated_resume: Dict,
        output_path: str,
        template_key: str = "ats_classic",
    ) -> str:

        template = get_template(
            template_key
        )

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        document = Document()

        DOCXResumeGenerator._configure_page(
            document
        )

        DOCXResumeGenerator._configure_styles(
            document
        )

        if template.columns == 1:

            DOCXResumeGenerator._build_single_column(
                document,
                generated_resume,
            )

        elif template.columns == 2:

            DOCXResumeGenerator._build_two_column(
                document,
                generated_resume,
            )

        else:

            raise ValueError(
                "Unsupported template column count."
            )

        document.save(
            str(output)
        )

        return str(output)

    # ======================================================
    # DOCUMENT CONFIGURATION
    # ======================================================

    @staticmethod
    def _configure_page(
        document: Document,
    ) -> None:

        section = document.sections[0]

        section.top_margin = Inches(0.55)
        section.bottom_margin = Inches(0.55)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    @staticmethod
    def _configure_styles(
        document: Document,
    ) -> None:

        normal = document.styles["Normal"]

        normal.font.name = "Arial"
        normal.font.size = Pt(9.5)

        normal.paragraph_format.space_after = Pt(2)

    # ======================================================
    # SINGLE COLUMN TEMPLATE
    # ======================================================

    @staticmethod
    def _build_single_column(
        document: Document,
        resume: Dict,
    ) -> None:

        DOCXResumeGenerator._add_header(
            document,
            resume,
        )

        DOCXResumeGenerator._add_summary(
            document,
            resume,
        )

        DOCXResumeGenerator._add_skills(
            document,
            resume,
        )

        DOCXResumeGenerator._add_experience(
            document,
            resume,
        )

        DOCXResumeGenerator._add_projects(
            document,
            resume,
        )

        DOCXResumeGenerator._add_education(
            document,
            resume,
        )

        DOCXResumeGenerator._add_certifications(
            document,
            resume,
        )

    # ======================================================
    # TWO COLUMN TEMPLATE
    # ======================================================

    @staticmethod
    def _build_two_column(
        document: Document,
        resume: Dict,
    ) -> None:

        DOCXResumeGenerator._add_header(
            document,
            resume,
        )

        DOCXResumeGenerator._enable_two_columns(
            document
        )

        # ----------------------------------------------
        # LEFT COLUMN
        # ----------------------------------------------

        DOCXResumeGenerator._add_contact_block(
            document,
            resume,
        )

        DOCXResumeGenerator._add_skills(
            document,
            resume,
        )

        DOCXResumeGenerator._add_education(
            document,
            resume,
        )

        DOCXResumeGenerator._add_certifications(
            document,
            resume,
        )

        # ----------------------------------------------
        # Move to right column
        # ----------------------------------------------

        DOCXResumeGenerator._add_column_break(
            document
        )

        # ----------------------------------------------
        # RIGHT COLUMN
        # ----------------------------------------------

        DOCXResumeGenerator._add_summary(
            document,
            resume,
        )

        DOCXResumeGenerator._add_experience(
            document,
            resume,
        )

        DOCXResumeGenerator._add_projects(
            document,
            resume,
        )

    # ======================================================
    # HEADER
    # ======================================================

    @staticmethod
    def _add_header(
        document: Document,
        resume: Dict,
    ) -> None:

        name = resume.get(
            "name",
            "",
        )

        paragraph = document.add_paragraph()

        paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )

        paragraph.paragraph_format.space_after = Pt(2)

        run = paragraph.add_run(name)

        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(18)

        # Target role if available
        target_role = resume.get(
            "target_role",
            "",
        )

        if target_role:

            paragraph = document.add_paragraph()

            paragraph.alignment = (
                WD_ALIGN_PARAGRAPH.CENTER
            )

            paragraph.paragraph_format.space_after = Pt(2)

            run = paragraph.add_run(
                target_role.upper()
            )

            run.bold = True
            run.font.size = Pt(10)

        DOCXResumeGenerator._add_contact_line(
            document,
            resume,
        )

    @staticmethod
    def _add_contact_line(
        document: Document,
        resume: Dict,
    ) -> None:

        values = [
            resume.get("email", ""),
            resume.get("phone", ""),
            resume.get("location", ""),
        ]

        values = [
            value
            for value in values
            if value
        ]

        if not values:
            return

        paragraph = document.add_paragraph()

        paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )

        run = paragraph.add_run(
            " | ".join(values)
        )

        run.font.size = Pt(8.5)

        links = resume.get(
            "links",
            [],
        )

        if links:

            paragraph = document.add_paragraph()

            paragraph.alignment = (
                WD_ALIGN_PARAGRAPH.CENTER
            )

            run = paragraph.add_run(
                " | ".join(links)
            )

            run.font.size = Pt(8.5)

    @staticmethod
    def _add_contact_block(
        document: Document,
        resume: Dict,
    ) -> None:

        values = [
            resume.get("email", ""),
            resume.get("phone", ""),
            resume.get("location", ""),
        ]

        values = [
            value
            for value in values
            if value
        ]

        if values:

            DOCXResumeGenerator._add_heading(
                document,
                "Contact",
            )

            for value in values:

                paragraph = document.add_paragraph(
                    value
                )

                paragraph.paragraph_format.space_after = Pt(1)

        links = resume.get(
            "links",
            [],
        )

        if links:

            DOCXResumeGenerator._add_heading(
                document,
                "Links",
            )

            for link in links:

                paragraph = document.add_paragraph(
                    link
                )

                paragraph.paragraph_format.space_after = Pt(1)

    # ======================================================
    # SUMMARY
    # ======================================================

    @staticmethod
    def _add_summary(
        document: Document,
        resume: Dict,
    ) -> None:

        summary = resume.get(
            "summary",
            "",
        )

        if not summary:
            return

        DOCXResumeGenerator._add_heading(
            document,
            "Professional Summary",
        )

        paragraph = document.add_paragraph(
            summary
        )

        paragraph.paragraph_format.space_after = Pt(3)

    # ======================================================
    # SKILLS
    # ======================================================

    @staticmethod
    def _add_skills(
        document: Document,
        resume: Dict,
    ) -> None:

        skills = resume.get(
            "skills",
            [],
        )

        if not skills:
            return

        DOCXResumeGenerator._add_heading(
            document,
            "Technical Skills",
        )

        paragraph = document.add_paragraph(
            ", ".join(skills)
        )

        paragraph.paragraph_format.space_after = Pt(3)

    # ======================================================
    # EXPERIENCE
    # ======================================================

    @staticmethod
    def _add_experience(
        document: Document,
        resume: Dict,
    ) -> None:

        experience = resume.get(
            "experience",
            [],
        )

        if not experience:
            return

        DOCXResumeGenerator._add_heading(
            document,
            "Experience",
        )

        for item in experience:

            role = item.get(
                "role",
                "",
            )

            company = item.get(
                "company",
                "",
            )

            duration = item.get(
                "duration",
                "",
            )

            values = [
                role,
                company,
                duration,
            ]

            values = [
                value
                for value in values
                if value
            ]

            if values:

                paragraph = document.add_paragraph()

                paragraph.paragraph_format.space_after = Pt(1)

                run = paragraph.add_run(
                    " | ".join(values)
                )

                run.bold = True
                run.font.size = Pt(9.5)

            for bullet in item.get(
                "bullets",
                [],
            ):

                DOCXResumeGenerator._add_bullet(
                    document,
                    bullet,
                )

    # ======================================================
    # PROJECTS
    # ======================================================

    @staticmethod
    def _add_projects(
        document: Document,
        resume: Dict,
    ) -> None:

        projects = resume.get(
            "projects",
            [],
        )

        if not projects:
            return

        DOCXResumeGenerator._add_heading(
            document,
            "Projects",
        )

        for project in projects:

            name = project.get(
                "name",
                "",
            )

            if name:

                paragraph = document.add_paragraph()

                paragraph.paragraph_format.space_after = Pt(1)

                run = paragraph.add_run(name)

                run.bold = True
                run.font.size = Pt(9.5)

            description = project.get(
                "description",
                "",
            )

            if description:

                paragraph = document.add_paragraph(
                    description
                )

                paragraph.paragraph_format.space_after = Pt(1)

            technologies = project.get(
                "technologies",
                [],
            )

            if technologies:

                paragraph = document.add_paragraph()

                run = paragraph.add_run(
                    "Technologies: "
                    + ", ".join(
                        technologies
                    )
                )

                run.italic = True
                run.font.size = Pt(8.5)

            for bullet in project.get(
                "bullets",
                [],
            ):

                DOCXResumeGenerator._add_bullet(
                    document,
                    bullet,
                )

    # ======================================================
    # EDUCATION
    # ======================================================

    @staticmethod
    def _add_education(
        document: Document,
        resume: Dict,
    ) -> None:

        education = resume.get(
            "education",
            [],
        )

        if not education:
            return

        DOCXResumeGenerator._add_heading(
            document,
            "Education",
        )

        for item in education:

            degree = item.get(
                "degree",
                "",
            )

            institution = item.get(
                "institution",
                "",
            )

            duration = item.get(
                "duration",
                "",
            )

            values = [
                degree,
                institution,
                duration,
            ]

            values = [
                value
                for value in values
                if value
            ]

            if values:

                paragraph = document.add_paragraph(
                    " | ".join(values)
                )

                paragraph.paragraph_format.space_after = Pt(2)

    # ======================================================
    # CERTIFICATIONS
    # ======================================================

    @staticmethod
    def _add_certifications(
        document: Document,
        resume: Dict,
    ) -> None:

        certifications = resume.get(
            "certifications",
            [],
        )

        if not certifications:
            return

        DOCXResumeGenerator._add_heading(
            document,
            "Certifications",
        )

        for certification in certifications:

            DOCXResumeGenerator._add_bullet(
                document,
                certification,
            )

    # ======================================================
    # FORMATTING HELPERS
    # ======================================================

    @staticmethod
    def _add_heading(
        document: Document,
        title: str,
    ) -> None:

        paragraph = document.add_paragraph()

        paragraph.paragraph_format.space_before = Pt(5)
        paragraph.paragraph_format.space_after = Pt(2)

        run = paragraph.add_run(
            title.upper()
        )

        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(10.5)

    @staticmethod
    def _add_bullet(
        document: Document,
        text: str,
    ) -> None:

        paragraph = document.add_paragraph(
            style="List Bullet"
        )

        paragraph.paragraph_format.left_indent = Inches(
            0.18
        )

        paragraph.paragraph_format.first_line_indent = Inches(
            -0.12
        )

        paragraph.paragraph_format.space_after = Pt(1)

        run = paragraph.add_run(text)

        run.font.name = "Arial"
        run.font.size = Pt(9)

    # ======================================================
    # TWO-COLUMN WORD XML
    # ======================================================

    @staticmethod
    def _enable_two_columns(
        document: Document,
    ) -> None:

        section = document.sections[0]

        sect_pr = section._sectPr

        columns = OxmlElement("w:cols")

        columns.set(
            qn("w:num"),
            "2",
        )

        columns.set(
            qn("w:space"),
            "720",
        )

        sect_pr.append(
            columns
        )

    @staticmethod
    def _add_column_break(
        document: Document,
    ) -> None:

        paragraph = document.add_paragraph()

        run = paragraph.add_run()

        break_element = OxmlElement(
            "w:br"
        )

        break_element.set(
            qn("w:type"),
            "column",
        )

        run._r.append(
            break_element
        )