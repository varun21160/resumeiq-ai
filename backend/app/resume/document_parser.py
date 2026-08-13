from pathlib import Path

from app.resume.docx_parser import DOCXParser
from app.resume.pdf_parser import PDFParser
from app.resume.text_cleaner import TextCleaner


class DocumentParser:
    """
    Main resume document parser.

    Supported formats:
        - PDF
        - DOCX

    Flow:

        File
          ↓
        Validate
          ↓
        Detect extension
          ↓
        PDFParser / DOCXParser
          ↓
        TextCleaner
          ↓
        Clean resume text
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
        """
        Extract and clean text from a resume document.

        Args:
            file_path:
                Path to the resume file.

        Returns:
            Cleaned resume text.

        Raises:
            FileNotFoundError:
                Resume file does not exist.

            ValueError:
                Invalid file, unsupported format, extraction failure,
                or empty extracted text.
        """

        # ---------------------------------------------------------
        # Validate input
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # Validate extension
        # ---------------------------------------------------------

        extension = path.suffix.lower()

        if extension not in cls.SUPPORTED_EXTENSIONS:
            supported = ", ".join(
                sorted(cls.SUPPORTED_EXTENSIONS)
            )

            raise ValueError(
                f"Unsupported resume format. "
                f"Supported formats: {supported}"
            )

        # ---------------------------------------------------------
        # Validate file size
        # ---------------------------------------------------------

        if path.stat().st_size == 0:
            raise ValueError(
                "The resume file is empty."
            )

        # ---------------------------------------------------------
        # Extract raw text
        # ---------------------------------------------------------

        try:

            if extension == ".pdf":

                raw_text = PDFParser.extract(
                    str(path)
                )

            elif extension == ".docx":

                raw_text = DOCXParser.extract(
                    str(path)
                )

            else:
                # Defensive check. This should never be reached
                # because extension validation happens above.
                raise ValueError(
                    f"Unsupported file type: {extension}"
                )

        except FileNotFoundError:
            raise

        except ValueError:
            raise

        except Exception as exc:
            raise ValueError(
                "Unable to extract text from the resume."
            ) from exc

        # ---------------------------------------------------------
        # Validate extracted text
        # ---------------------------------------------------------

        if not raw_text or not raw_text.strip():
            raise ValueError(
                "Resume contains no readable text."
            )

        # ---------------------------------------------------------
        # Clean extracted text
        # ---------------------------------------------------------

        try:

            cleaned_text = TextCleaner.clean(
                raw_text
            )

        except Exception as exc:
            raise ValueError(
                "Unable to clean the extracted resume text."
            ) from exc

        # ---------------------------------------------------------
        # Final validation
        # ---------------------------------------------------------

        if not cleaned_text or not cleaned_text.strip():
            raise ValueError(
                "Resume contains no readable text after cleaning."
            )

        return cleaned_text.strip()