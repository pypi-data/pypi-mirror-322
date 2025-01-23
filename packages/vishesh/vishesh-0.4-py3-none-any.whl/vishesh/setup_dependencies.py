# vishesh/setup_dependencies.py
import subprocess
import sys

def setup_dependencies():
    dependencies = ["requests"]  # Add any other dependencies here
    for dependency in dependencies:
        print(f"Installing {dependency}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dependency])
    print("All dependencies installed successfully!")
