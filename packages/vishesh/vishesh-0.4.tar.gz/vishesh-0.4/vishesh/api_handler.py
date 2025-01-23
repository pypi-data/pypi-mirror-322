import requests
import os
import json

# Updated API base URL for Gemini
API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# API Key for authentication
API_KEY = "AIzaSyCokKdmFp7GEqOB-TBdF858t85CwFWGirk"

def fetch_problem_data(question_number):
    """
    Fetch problem data for a specific LeetCode question using the Gemini API.

    Parameters:
        question_number (int): The LeetCode question number.

    Returns:
        dict: A dictionary with the parsed response data if successful, None otherwise.
    """
    url = f"{API_BASE_URL}?key={API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": f"LeetCode problem {question_number}: Provide a description, Solution approach and solutions in Python, C++, and Java."}]
        }]
    }
    headers = {"Content-Type": "application/json"}

    try:
        # Make the POST request to the Gemini API
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        data = response.json()

        # Extract the problem description and solutions
        content_parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])

        problem_description = ""
        solution_description = ""
        python_code = ""
        cpp_code = ""
        java_code = ""

        for part in content_parts:
            text = part.get('text', '')
            if 'description' in text.lower():
                problem_description = text
            elif 'solution' in text.lower():
                solution_description = text
            elif 'python' in text.lower():
                python_code = text
            elif 'c++' in text.lower():
                cpp_code = text
            elif 'java' in text.lower():
                java_code = text

        return {
            "question_description": problem_description,
            "solution_description": solution_description,
            "python_code": python_code,
            "cpp_code": cpp_code,
            "java_code": java_code
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for question {question_number}: {e}")
        return None
