from typing import Any, Dict, List


class ReportGenerator:
    """
    Turns structured LinkedIn analysis JSON into a readable text report.
    """

    def generate_report(self, analysis: Dict[str, Any]) -> str:
        lines: List[str] = []

        overall_score = analysis.get("overall_score", "N/A")
        strengths = analysis.get("strengths", [])

        lines.append("LINKEDIN PROFILE COACH REPORT")
        lines.append("=" * 32)
        lines.append(f"Overall Score: {overall_score}/100")
        lines.append("")

        if strengths:
            lines.append("Strengths")
            lines.append("-" * 9)
            for strength in strengths:
                lines.append(f"- {strength}")
            lines.append("")

        lines.extend(self._format_section("Headline", analysis.get("headline", {})))
        lines.extend(self._format_section("About", analysis.get("about", {})))
        lines.extend(self._format_section("Experience", analysis.get("experience", {})))
        lines.extend(self._format_section("Skills", analysis.get("skills", {})))
        lines.extend(self._format_section("Featured", analysis.get("featured", {})))
        lines.extend(self._format_section("Banner", analysis.get("banner", {})))
        lines.extend(self._format_completeness_section(analysis.get("completeness", {})))

        return "\n".join(lines).strip()

    def _format_section(self, title: str, section_data: Dict[str, Any]) -> List[str]:
        lines: List[str] = []

        if not section_data:
            return lines

        score = section_data.get("score", "N/A")
        lines.append(title)
        lines.append("-" * len(title))
        lines.append(f"Score: {score}/100")

        if section_data.get("missing") is True:
            lines.append("Status: Missing")

        issues = section_data.get("issues", [])
        if issues:
            lines.append("Issues:")
            for issue in issues:
                lines.append(f"- {issue}")

        strong_profile_notes = section_data.get("what_strong_profiles_do", [])
        if strong_profile_notes:
            lines.append("What strong profiles do:")
            for note in strong_profile_notes:
                lines.append(f"- {note}")

        rewrite = section_data.get("rewrite", "")
        if rewrite:
            lines.append("Suggested rewrite:")
            lines.append(rewrite)

        rewrite_suggestions = section_data.get("rewrite_suggestions", [])
        if rewrite_suggestions:
            lines.append("Rewrite suggestions:")
            for suggestion in rewrite_suggestions:
                lines.append(f"- {suggestion}")

        suggested_skills = section_data.get("suggested_skills", [])
        if suggested_skills:
            lines.append("Suggested skills:")
            for skill in suggested_skills:
                lines.append(f"- {skill}")

        suggestions = section_data.get("suggestions", [])
        if suggestions:
            lines.append("Suggestions:")
            for suggestion in suggestions:
                lines.append(f"- {suggestion}")

        ai_banner_prompt = section_data.get("ai_banner_prompt", "")
        if ai_banner_prompt:
            lines.append("AI banner prompt:")
            lines.append(ai_banner_prompt)

        lines.append("")
        return lines

    def _format_completeness_section(self, completeness_data: Dict[str, Any]) -> List[str]:
        lines: List[str] = []

        if not completeness_data:
            return lines

        lines.append("Completeness")
        lines.append("-" * 12)

        missing_sections = completeness_data.get("missing_sections", [])
        if missing_sections:
            lines.append("Missing sections:")
            for section in missing_sections:
                lines.append(f"- {section}")

        suggestions_to_add_later = completeness_data.get("suggestions_to_add_later", [])
        if suggestions_to_add_later:
            lines.append("Suggestions to add later:")
            for suggestion in suggestions_to_add_later:
                lines.append(f"- {suggestion}")

        lines.append("")
        return lines
