import os

def save_problem_files(question_number, data):
    # Create a folder for the problem
    folder_name = f"leetcode-{question_number}"
    os.makedirs(folder_name, exist_ok=True)

    # Fetch Question Description and save it to the file
    question_description = data.get("question_description", "No description available")
    with open(os.path.join(folder_name, "1.Solution.md"), "w") as question_file:
        question_file.write(question_description)

    print(f"Problem {question_number} files saved in {folder_name}")  