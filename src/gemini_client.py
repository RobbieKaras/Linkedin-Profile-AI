import os
from typing import Optional

from google import genai
from google.genai import types


class GeminiClient:
    """
    Small wrapper around the Gemini API client.
    Handles API key setup and text / JSON generation.
    """

    def __init__(self, model: Optional[str] = None) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        if not self.api_key:
            raise ValueError("Missing GEMINI_API_KEY. Add it to your .env file.")

        self.client = genai.Client(api_key=self.api_key)

    def generate_text(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return plain text output.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.5,
            ),
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()

    def generate_json(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and request JSON output.
        Returns the raw text response.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.4,
            ),
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()
