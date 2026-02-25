import sys
import subprocess
import os

def format_batch(directory):
    print(f"Formatting {directory}...")
    try:
        # Run isort
        subprocess.run([sys.executable, "-m", "isort", directory], check=True)
        # Run black
        subprocess.run([sys.executable, "-m", "black", directory], check=True)
        # Run ruff check --fix
        subprocess.run([sys.executable, "-m", "ruff", "check", directory, "--fix", "--output-format=concise", "--no-cache"], check=False)
        print(f"Successfully processed {directory}")
    except Exception as e:
        print(f"Error processing {directory}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        format_batch(sys.argv[1])
    else:
        print("Please provide a directory")
