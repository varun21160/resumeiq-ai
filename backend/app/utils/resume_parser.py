from pathlib import Path
import fitz  # PyMuPDF
from docx import Document


class ResumeParser:

    @staticmethod
    def extract_text(file_path: str) -> str:
        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return ResumeParser._extract_pdf(file_path)

        elif extension == ".docx":
            return ResumeParser._extract_docx(file_path)

        raise ValueError("Unsupported file type")

    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        text = ""

        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()

        return text.strip()

    @staticmethod
    def _extract_docx(file_path: str) -> str:
        document = Document(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return text.strip()