import sys

from src.gemini_client import GeminiClient
from src.analyzer import LinkedInProfileAnalyzer
from src.report_generator import ReportGenerator


def read_profile_input() -> str:
    """
    Prompts the user to paste their LinkedIn profile text.
    """
    print("\nPaste your LinkedIn profile text below.")
    print("When finished, press ENTER twice.\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "" and len(lines) > 0:
            break
        lines.append(line)

    return "\n".join(lines)


def main():
    print("LinkedIn Profile Coach AI")
    print("=" * 26)

    try:
        profile_text = read_profile_input()

        if not profile_text.strip():
            print("No profile text provided.")
            sys.exit(1)

        # Initialize components
        gemini_client = GeminiClient()
        analyzer = LinkedInProfileAnalyzer(gemini_client)
        report_generator = ReportGenerator()

        print("\nAnalyzing profile...\n")

        # Analyze profile
        analysis = analyzer.analyze_profile(profile_text)

        # Generate readable report
        report = report_generator.generate_report(analysis)

        print(report)

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

    except Exception as e:
        print("\nError occurred:")
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
