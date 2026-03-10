from dotenv import load_dotenv
load_dotenv()

import sys

from src.gemini_client import GeminiClient
from src.analyzer import LinkedInProfileAnalyzer
from src.report_generator import ReportGenerator


def read_profile_input() -> str:
    """
    Prompt the user to paste LinkedIn profile text.
    Input ends after two Enter presses in a row.
    """
    print("\nPaste your LinkedIn profile text below.")
    print("When finished, press ENTER on a blank line.\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "" and lines:
            break
        lines.append(line)

    return "\n".join(lines).strip()


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
