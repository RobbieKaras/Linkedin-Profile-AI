import json
from typing import Any, Dict

from src.gemini_client import GeminiClient


class LinkedInProfileAnalyzer:
    """
    Builds the LinkedIn coaching prompt and asks Gemini
    for structured feedback in JSON format.
    """

    def __init__(self, gemini_client: GeminiClient) -> None:
        self.gemini_client = gemini_client

    def analyze_profile(self, profile_text: str) -> Dict[str, Any]:
        """
        Analyze a user's LinkedIn profile text and return structured JSON.
        """
        if not profile_text or not profile_text.strip():
            raise ValueError("Profile text cannot be empty.")

        prompt = self._build_prompt(profile_text)
        raw_response = self.gemini_client.generate_json(prompt)
        return self._parse_json_response(raw_response)

    def _build_prompt(self, profile_text: str) -> str:
        return f"""
You are an AI LinkedIn Profile Coach.

Your job is to help users learn how to present themselves better on LinkedIn.
Do not just rewrite sections. Teach the user why a section is weak,
how strong profiles are structured, and what they can improve later.

You must analyze the profile in these areas:
1. headline
2. about section
3. experience
4. skills
5. featured section
6. banner / visual branding
7. overall completeness

Important guidance:
- Reward clarity, professionalism, keyword usage, direction, and structure.
- Penalize vague wording, weak headlines, missing sections, poor keyword use,
  lack of technical detail, and lack of direction.
- If the user is a student, suggest ways to present education, clubs,
  projects, certifications, and early experience more professionally.
- If the profile is missing an About section, say so clearly.
- If the Featured section is missing, suggest adding a resume, GitHub, portfolio,
  or strong project.
- If the banner seems generic or missing, suggest creating a professional banner.
- For banner suggestions, recommend using AI image tools to generate one based on
  the user's school, major, and career interests.
- If multiple roles in one organization suggest growth, mention that showing
  progression is valuable.
- Give practical suggestions, not vague motivational advice.
- Be constructive and specific.

Return ONLY valid JSON.
Do not include markdown fences.
Do not include any explanation outside the JSON.

Use this exact JSON structure:
{{
  "overall_score": 0,
  "strengths": [],
  "headline": {{
    "score": 0,
    "issues": [],
    "what_strong_profiles_do": [],
    "rewrite": ""
  }},
  "about": {{
    "score": 0,
    "issues": [],
    "what_strong_profiles_do": [],
    "rewrite": "",
    "missing": false
  }},
  "experience": {{
    "score": 0,
    "issues": [],
    "what_strong_profiles_do": [],
    "rewrite_suggestions": []
  }},
  "skills": {{
    "score": 0,
    "issues": [],
    "what_strong_profiles_do": [],
    "suggested_skills": []
  }},
  "featured": {{
    "score": 0,
    "issues": [],
    "what_strong_profiles_do": [],
    "suggestions": [],
    "missing": false
  }},
  "banner": {{
    "score": 0,
    "issues": [],
    "what_strong_profiles_do": [],
    "suggestions": [],
    "ai_banner_prompt": ""
  }},
  "completeness": {{
    "missing_sections": [],
    "suggestions_to_add_later": []
  }}
}}

Here is the LinkedIn profile content to analyze:

{profile_text}
""".strip()

    def _parse_json_response(self, raw_response: str) -> Dict[str, Any]:
        """
        Parse Gemini output as JSON.
        Tries direct parsing first, then attempts recovery
        if extra text appears around the JSON.
        """
        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            cleaned = raw_response.strip()

            start = cleaned.find("{")
            end = cleaned.rfind("}")

            if start == -1 or end == -1 or end <= start:
                raise ValueError(
                    "Model response was not valid JSON and could not be recovered."
                )

            possible_json = cleaned[start:end + 1]

            try:
                return json.loads(possible_json)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Model response looked like JSON but could not be parsed."
                ) from exc
