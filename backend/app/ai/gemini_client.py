import google.generativeai as genai

from app.core.config import settings


class GeminiClient:
    """
    Wrapper around the Gemini API.
    Responsible only for communicating with Gemini.
    """

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)

        self.model = genai.GenerativeModel(
            settings.GEMINI_MODEL
        )

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the response text.
        """
        response = self.model.generate_content(prompt)

        return response.text.strip()


gemini_client = GeminiClient()