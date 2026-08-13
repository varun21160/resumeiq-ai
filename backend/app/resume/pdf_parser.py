from pathlib import Path

from pypdf import PdfReader


class PDFParser:
    """
    Extracts text from PDF resume files.
    """

    @staticmethod
    def extract(file_path: str) -> str:
        """
        Extract text from all pages of a PDF.

        Raises:
            FileNotFoundError:
                If the file does not exist.

            ValueError:
                If the file is invalid, unreadable, or contains no
                extractable text.
        """

        if not file_path:
            raise ValueError(
                "Resume file path is required."
            )

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Resume file not found: {file_path}"
            )

        if not path.is_file():
            raise ValueError(
                "The provided resume path is not a file."
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                "PDFParser only supports PDF files."
            )

        if path.stat().st_size == 0:
            raise ValueError(
                "The PDF resume file is empty."
            )

        try:
            reader = PdfReader(str(path))
        except Exception as exc:
            raise ValueError(
                "Unable to read the PDF resume. "
                "The file may be corrupted or invalid."
            ) from exc

        if not reader.pages:
            raise ValueError(
                "The PDF resume contains no pages."
            )

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""

            if text.strip():
                pages.append(text.strip())

        extracted_text = "\n".join(pages).strip()

        if not extracted_text:
            raise ValueError(
                "No readable text was found in the PDF. "
                "The resume may be image-based or scanned."
            )

        return extracted_text