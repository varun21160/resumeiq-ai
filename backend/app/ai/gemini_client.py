import time

from google import genai

from app.core.config import settings


class GeminiClient:
    """
    Wrapper around the Gemini API.

    Responsible only for communication with Gemini.
    """

    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 2

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to Gemini and return the generated text.

        Retries temporary API failures such as 503 errors.
        """

        if not prompt or not prompt.strip():
            raise ValueError(
                "Gemini prompt cannot be empty."
            )

        last_error = None

        for attempt in range(
            1,
            self.MAX_RETRIES + 1,
        ):
            try:
                response = (
                    self.client.models.generate_content(
                        model=self.model,
                        contents=prompt,
                    )
                )

                if not response or not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return response.text.strip()

            except Exception as exc:
                last_error = exc

                if attempt < self.MAX_RETRIES:
                    time.sleep(
                        self.RETRY_DELAY_SECONDS * attempt
                    )

        raise RuntimeError(
            f"Gemini API request failed after "
            f"{self.MAX_RETRIES} attempts: {last_error}"
        ) from last_error


gemini_client = GeminiClient()