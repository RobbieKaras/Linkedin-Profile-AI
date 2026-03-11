from typing import Any, Dict

from src.gemini_client import GeminiClient


class PostAnalysisAssistant:
    """
    Handles follow-up actions after the main profile report is generated.
    """

    def __init__(self, gemini_client: GeminiClient) -> None:
        self.gemini_client = gemini_client

    def generate_improvement_plan(
        self,
        profile_text: str,
        analysis: Dict[str, Any],
    ) -> str:
        prompt = f"""
You are an AI LinkedIn coach.

The user has already received a profile analysis.
Your job is to create a practical, step-by-step improvement plan.

Rules:
- Be specific and actionable.
- Organize the plan into numbered steps.
- Prioritize the highest-impact fixes first.
- Explain what to fix, why it matters, and exactly what to do.
- Include concrete examples where helpful.
- End with a short "quick wins" section.
- Write clearly and professionally.

Profile text:
{profile_text}

Analysis JSON:
{analysis}
""".strip()

        return self.gemini_client.generate_text(prompt)

    def generate_targeted_improvements(
        self,
        profile_text: str,
        analysis: Dict[str, Any],
    ) -> str:
        prompt = f"""
You are an AI LinkedIn coach.

Based on the user's profile and analysis, suggest high-value improvements
they can make outside of rewriting text.

Rules:
- Identify likely career direction from the profile.
- Suggest useful additions such as projects, featured items, certifications,
  profile sections, portfolio links, and skills.
- If the user appears interested in cybersecurity, suggest LinkedIn Learning
  or similar certificate/course ideas relevant to cybersecurity, networking,
  Linux, SOC work, threat detection, or security fundamentals.
- If the user appears interested in software or AI, suggest fitting course or
  certificate ideas for those paths instead.
- Do not invent exact course URLs.
- Present the output as clean sections with bullet points.
- Be practical and tailored.

Profile text:
{profile_text}

Analysis JSON:
{analysis}
""".strip()

        return self.gemini_client.generate_text(prompt)

    def generate_improved_profile(
        self,
        profile_text: str,
        analysis: Dict[str, Any],
    ) -> str:
        prompt = f"""
You are an AI LinkedIn profile writer.

Your job is to generate an improved version of the user's LinkedIn profile
based on their current profile and analysis.

Rules:
- Keep the output realistic and based on the user's background.
- Do not invent fake jobs, fake skills, fake projects, fake metrics, or fake certifications.
- Improve presentation, clarity, professionalism, and keyword usage.
- Include these sections if possible:
  1. Headline
  2. About
  3. Experience rewrites
  4. Suggested skills
  5. Featured section ideas
  6. Banner suggestion
- If information is missing, use placeholders like:
  [Add project name here]
  [Add measurable result here]
- Make it easy for the user to copy into LinkedIn.

Profile text:
{profile_text}

Analysis JSON:
{analysis}
""".strip()

        return self.gemini_client.generate_text(prompt)

    def chat_about_profile(
        self,
        profile_text: str,
        analysis: Dict[str, Any],
        question: str,
    ) -> str:
        prompt = f"""
You are an AI LinkedIn coach helping a user improve their profile.

Answer the user's question using the profile text and prior analysis.
Be specific, practical, and concise.

Profile text:
{profile_text}

Analysis JSON:
{analysis}

User question:
{question}
""".strip()

        return self.gemini_client.generate_text(prompt)
