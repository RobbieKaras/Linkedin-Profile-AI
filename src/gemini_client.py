import os
from typing import Optional

from google import genai


class GeminiClient:
    """
    Small wrapper around the Gemini API client.
    Keeps API setup separate from the rest of the project.
    """

    def __init__(self, model: str = "gemini-3-flash-preview") -> None:
        self.api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.model = model

        if not self.api_key:
            raise ValueError(
                "Missing GEMINI_API_KEY. Add it to your environment or .env file."
            )

        self.client = genai.Client(api_key=self.api_key)

    def generate_text(self, prompt: str) -> str:
        """
        Sends a prompt to Gemini and returns plain text output.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()
