import os
import csv


class LinkedInDataParser:

    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    def parse(self) -> str:
        """
        Reads LinkedIn export CSV files and builds a text profile.
        """

        sections = []

        sections.append(self._parse_profile())
        sections.append(self._parse_positions())
        sections.append(self._parse_skills())
        sections.append(self._parse_education())

        return "\n\n".join([s for s in sections if s])

    def _read_csv(self, filename):
        path = os.path.join(self.folder_path, filename)

        if not os.path.exists(path):
            return []

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _parse_profile(self):
        rows = self._read_csv("Profile.csv")

        if not rows:
            return ""

        r = rows[0]

        headline = r.get("Headline", "")
        summary = r.get("Summary", "")

        return f"""
Headline:
{headline}

About:
{summary}
""".strip()

    def _parse_positions(self):
        rows = self._read_csv("Positions.csv")

        if not rows:
            return ""

        lines = ["Experience:"]

        for r in rows:

            title = r.get("Title", "")
            company = r.get("Company Name", "")
            desc = r.get("Description", "")

            lines.append(f"- {title} at {company}")
            if desc:
                lines.append(f"  {desc}")

        return "\n".join(lines)

    def _parse_skills(self):
        rows = self._read_csv("Skills.csv")

        if not rows:
            return ""

        skills = [r.get("Name", "") for r in rows]

        return "Skills:\n" + ", ".join(skills)

    def _parse_education(self):
        rows = self._read_csv("Education.csv")

        if not rows:
            return ""

        lines = ["Education:"]

        for r in rows:

            school = r.get("School Name", "")
            degree = r.get("Degree Name", "")
            field = r.get("Field Of Study", "")

            lines.append(f"- {degree} in {field} at {school}")

        return "\n".join(lines)
