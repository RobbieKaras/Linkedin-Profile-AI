from dotenv import load_dotenv
load_dotenv()

import os
import sys
from datetime import datetime

from src.gemini_client import GeminiClient
from src.analyzer import LinkedInProfileAnalyzer
from src.report_generator import ReportGenerator
from src.linkedin_parser import LinkedInDataParser
from src.post_analysis import PostAnalysisAssistant


def choose_input_method() -> str:
    print("\nChoose how you want to provide your LinkedIn data:\n")
    print("1) Paste profile text")
    print("2) Use LinkedIn data export folder\n")

    choice = input("Enter 1 or 2: ").strip()

    if choice not in ["1", "2"]:
        print("Invalid choice.")
        sys.exit(1)

    return choice


def read_profile_input() -> str:
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


def get_linkedin_folder() -> str:
    print("\nEnter the path to your LinkedIn export folder.\n")

    folder = input("LinkedIn export folder path: ").strip()

    if not os.path.isdir(folder):
        print("Error: That folder does not exist.")
        sys.exit(1)

    return folder


def ask_to_save_report() -> bool:
    print("\nWould you like to save this report to a file?")
    print("1) Yes")
    print("2) No\n")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        return True
    if choice == "2":
        return False

    print("Invalid choice.")
    sys.exit(1)


def save_text_output(content: str, prefix: str) -> str:
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(output_dir, f"{prefix}_{timestamp}.md")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return file_path


def post_report_menu() -> str:
    print("\nWhat would you like to do next?\n")
    print("1) Get step-by-step improvement plan")
    print("2) Get targeted improvement ideas and certificate suggestions")
    print("3) Chat with AI about your profile")
    print("4) Generate improved LinkedIn profile")
    print("5) Exit\n")

    choice = input("Enter 1, 2, 3, 4, or 5: ").strip()

    if choice not in ["1", "2", "3", "4", "5"]:
        print("Invalid choice.")
        return "5"

    return choice


def handle_follow_up_actions(
    assistant: PostAnalysisAssistant,
    profile_text: str,
    analysis: dict,
) -> None:
    while True:
        choice = post_report_menu()

        if choice == "1":
            print("\nGenerating step-by-step improvement plan...\n")
            plan = assistant.generate_improvement_plan(profile_text, analysis)
            print(plan)

            if ask_to_save_report():
                saved_file = save_text_output(
                    plan,
                    "linkedin_improvement_plan",
                )
                print(f"\nSaved to: {saved_file}")

        elif choice == "2":
            print("\nGenerating targeted improvement ideas...\n")
            suggestions = assistant.generate_targeted_improvements(
                profile_text,
                analysis,
            )
            print(suggestions)

            if ask_to_save_report():
                saved_file = save_text_output(
                    suggestions,
                    "linkedin_targeted_improvements",
                )
                print(f"\nSaved to: {saved_file}")

        elif choice == "3":
            print("\nChat mode started.")
            print("Ask questions about your profile.")
            print("Type 'exit' to return to the menu.\n")

            while True:
                question = input("You: ").strip()

                if question.lower() == "exit":
                    print("")
                    break

                if not question:
                    continue

                response = assistant.chat_about_profile(
                    profile_text,
                    analysis,
                    question,
                )
                print(f"\nAI:\n{response}\n")

        elif choice == "4":
            print("\nGenerating improved LinkedIn profile...\n")
            improved_profile = assistant.generate_improved_profile(
                profile_text,
                analysis,
            )
            print(improved_profile)

            if ask_to_save_report():
                saved_file = save_text_output(
                    improved_profile,
                    "improved_linkedin_profile",
                )
                print(f"\nSaved to: {saved_file}")

        elif choice == "5":
            print("\nGoodbye.")
            break


def main() -> None:
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
        post_analysis_assistant = PostAnalysisAssistant(gemini_client)

        print("\nAnalyzing profile with AI...\n")

        analysis = analyzer.analyze_profile(profile_text)
        report = report_generator.generate_report(analysis)

        print(report)

        if ask_to_save_report():
            saved_file = save_text_output(
                "# LinkedIn Profile Coach Report\n\n```text\n" + report + "\n```",
                "linkedin_profile_report",
            )
            print(f"\nReport saved to: {saved_file}")
        else:
            print("\nReport was not saved.")

        handle_follow_up_actions(
            post_analysis_assistant,
            profile_text,
            analysis,
        )

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

    except Exception as e:
        print("\nError occurred:")
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
