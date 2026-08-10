from pathlib import Path

from docx import Document


class DOCXParser:
    """
    Extracts text from DOCX resume files.
    """

    @staticmethod
    def extract(file_path: str) -> str:
        """
        Extract text from paragraphs and tables in a DOCX file.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Resume file not found: {file_path}"
            )

        if path.suffix.lower() != ".docx":
            raise ValueError(
                "DOCXParser only supports DOCX files."
            )

        try:
            document = Document(str(path))
        except Exception as exc:
            raise ValueError(
                "Unable to read the DOCX resume."
            ) from exc

        sections = []

        # Normal paragraphs
        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                sections.append(text)

        # Tables are common in resumes, so we must not ignore them.
        for table in document.tables:
            for row in table.rows:
                cells = []

                for cell in row.cells:
                    text = cell.text.strip()

                    if text:
                        cells.append(text)

                if cells:
                    sections.append(" | ".join(cells))

        extracted_text = "\n".join(sections).strip()

        if not extracted_text:
            raise ValueError(
                "No readable text was found in the DOCX resume."
            )

        return extracted_text