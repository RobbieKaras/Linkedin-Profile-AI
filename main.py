from dotenv import load_dotenv
load_dotenv()

import sys
import os

from src.gemini_client import GeminiClient
from src.analyzer import LinkedInProfileAnalyzer
from src.report_generator import ReportGenerator
from src.linkedin_parser import LinkedInDataParser


def get_linkedin_folder():
    """
    Ask the user for the LinkedIn export folder path.
    """

    print("\nEnter the path to your LinkedIn export folder.")
    print("Example:")
    print("/Users/username/Downloads/LinkedInData")
    print("or")
    print("C:\\Users\\username\\Downloads\\LinkedInData\n")

    folder = input("LinkedIn export folder path: ").strip()

    if not os.path.isdir(folder):
        print("\nError: That folder does not exist.")
        sys.exit(1)

    return folder


def main():

    print("LinkedIn Profile Coach AI")
    print("=" * 26)

    try:

        folder = get_linkedin_folder()

        print("\nReading LinkedIn data...\n")

        parser = LinkedInDataParser(folder)
        profile_text = parser.parse()

        if not profile_text.strip():
            print("No usable profile data found in the LinkedIn export.")
            sys.exit(1)

        gemini_client = GeminiClient()
        analyzer = LinkedInProfileAnalyzer(gemini_client)
        report_generator = ReportGenerator()

        print("Analyzing profile with AI...\n")

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
