# vishesh/main.py
import sys
from vishesh.api_handler import fetch_problem_data
from vishesh.file_manager import save_problem_files
from vishesh.setup_dependencies import setup_dependencies

def main():
    if len(sys.argv) < 2:
        print("Usage: vishesh <command>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "leetcode-help-setup":
        setup_dependencies()

    elif command.startswith("leetcode-help-"):
        question_number = command.split("-")[-1]
        try:
            int(question_number)  # Ensure it's a number
        except ValueError:
            print("Invalid question number. Please provide a valid number.")
            sys.exit(1)

        data = fetch_problem_data(question_number)
        if data:
            save_problem_files(question_number, data)
        else:
            print("Failed to fetch problem data.")

    else:
        print("Invalid command. Available commands:")
        print("  - leetcode-help-setup")
        print("  - leetcode-help-<question_number>")
