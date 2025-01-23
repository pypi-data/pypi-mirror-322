import os
import requests
import sys

# Base URL for raw files from your GitHub repository
GITHUB_RAW_URL = "https://raw.githubusercontent.com/visheshj2005/leetcode/main/"

def fetch_program_from_github(filename):
    # Construct the full URL to fetch the program file from GitHub
    url = GITHUB_RAW_URL + filename
    response = requests.get(url)
    
    if response.status_code == 200:
        # Write the file content to the local system
        with open(filename, 'w') as file:
            file.write(response.text)
        print(f"File '{filename}' created successfully!")
    else:
        print(f"Error: Could not fetch {filename} from GitHub (status code {response.status_code})")

def main():
    # Get the filename argument passed by the user
    if len(sys.argv) != 2:
        print("Usage: vishesh <program_name>.py")
        sys.exit(1)

    filename = sys.argv[1]
    
    # Call the function to fetch the program file from GitHub
    fetch_program_from_github(filename)

if __name__ == "__main__":
    main()
