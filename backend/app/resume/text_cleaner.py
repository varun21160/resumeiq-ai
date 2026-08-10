import re


class TextCleaner:
    """
    Cleans extracted resume text while preserving
    useful resume structure.
    """

    @staticmethod
    def clean(text: str) -> str:
        if not text or not text.strip():
            return ""

        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove excessive spaces/tabs.
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        # Normalize excessive blank lines.
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        # Remove spaces around newlines.
        text = re.sub(
            r" *\n *",
            "\n",
            text,
        )

        return text.strip()