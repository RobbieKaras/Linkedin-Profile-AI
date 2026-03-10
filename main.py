from dotenv import load_dotenv
load_dotenv()

import sys
import os

from src.gemini_client import GeminiClient
from src.analyzer import LinkedInProfileAnalyzer
from src.report_generator import ReportGenerator
from src.linkedin_parser import LinkedInDataParser


def choose_input_method():
    print("\nChoose how you want to provide your LinkedIn data:\n")
    print("1) Paste profile text")
    print("2) Use LinkedIn data export folder\n")

    choice = input("Enter 1 or 2: ").strip()

    if choice not in ["1", "2"]:
        print("Invalid choice.")
        sys.exit(1)

    return choice


def read_profile_input():
    """
    Method 1: User pastes profile text
    """

    print("\nPaste your LinkedIn profile text below.")
    print("When finished press ENTER on a blank line.\n")

    lines = []

    while True:
        line = input()

        if line.strip() == "" and lines:
            break

        lines.append(line)

    profile_text = "\n".join(lines).strip()

    if not profile_text:
        print("No profile text provided.")
        sys.exit(1)

    return profile_text


def get_linkedin_folder():
    """
    Method 2: User provides LinkedIn export folder
    """

    print("\nEnter the path to your LinkedIn export folder.\n")

    folder = input("LinkedIn export folder path: ").strip()

    if not os.path.isdir(folder):
        print("Error: That folder does not exist.")
        sys.exit(1)

    return folder


def main():

    print("LinkedIn Profile Coach AI")
    print("=" * 26)

    try:

        method = choose_input_method()

        if method == "1":

            profile_text = read_profile_input()

        else:

            folder = get_linkedin_folder()

            print("\nReading LinkedIn export data...\n")

            parser = LinkedInDataParser(folder)
            profile_text = parser.parse()

        if not profile_text.strip():
            print("No usable profile data found.")
            sys.exit(1)

        gemini_client = GeminiClient()
        analyzer = LinkedInProfileAnalyzer(gemini_client)
        report_generator = ReportGenerator()

        print("\nAnalyzing profile with AI...\n")

        analysis = analyzer.analyze_profile(profile_text)

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
