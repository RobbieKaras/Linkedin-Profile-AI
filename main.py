from dotenv import load_dotenv
load_dotenv()

import sys

from src.gemini_client import GeminiClient
from src.analyzer import LinkedInProfileAnalyzer
from src.report_generator import ReportGenerator


def read_profile_input() -> str:
    """
    Prompt the user to paste LinkedIn profile text.
    Input ends after one blank line.
    """

    print("\nPaste your LinkedIn profile text below.")
    print("Do NOT paste a LinkedIn URL. Paste the actual text from your profile.\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "" and lines:
            break
        lines.append(line)

    profile_text = "\n".join(lines).strip()

    if "linkedin.com" in profile_text:
        print("\n⚠️  It looks like you pasted a LinkedIn URL.")
        print("This tool cannot read LinkedIn pages.")
        print("Please paste the actual profile text instead.\n")

    return profile_text


def main() -> None:
    print("LinkedIn Profile Coach AI")
    print("=" * 26)

    try:
        profile_text = read_profile_input()

        if not profile_text:
            print("No profile text provided.")
            sys.exit(1)

        gemini_client = GeminiClient()
        analyzer = LinkedInProfileAnalyzer(gemini_client)
        report_generator = ReportGenerator()

        print("\nAnalyzing profile...\n")

        analysis = analyzer.analyze_profile(profile_text)
        report = report_generator.generate_report(analysis)

        print(report)

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

    except Exception as exc:
        print("\nError occurred:")
        print(str(exc))
        sys.exit(1)


if __name__ == "__main__":
    main()
