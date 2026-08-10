from pathlib import Path

from app.resume.docx_parser import DOCXParser
from app.resume.pdf_parser import PDFParser
from app.resume.text_cleaner import TextCleaner


class DocumentParser:
    """
    Main resume document parser.

    Supports:
        - PDF
        - DOCX
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
    }

    @classmethod
    def extract_text(
        cls,
        file_path: str,
    ) -> str:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Resume file not found: {file_path}"
            )

        extension = path.suffix.lower()

        if extension not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(
                "Unsupported resume format. "
                "Only PDF and DOCX files are supported."
            )

        if extension == ".pdf":
            raw_text = PDFParser.extract(
                str(path)
            )

        elif extension == ".docx":
            raw_text = DOCXParser.extract(
                str(path)
            )

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        cleaned_text = TextCleaner.clean(
            raw_text
        )

        if not cleaned_text:
            raise ValueError(
                "Resume contains no readable text."
            )

        return cleaned_text