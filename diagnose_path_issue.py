import os
from pathlib import Path

def check_project_path():
    # Get current working directory
    cwd = os.getcwd()
    print(f"Current Working Directory: {cwd}")

    # Convert to absolute path and normalize
    abs_path = Path(cwd).resolve()
    print(f"Resolved Absolute Path: {abs_path}")

    # Check for incorrect formatting
    raw_path = str(abs_path)
    if "\\" in raw_path:
        print("✔ Detected Windows-style backslashes. Good.")
    else:
        print("❌ Warning: Path may be malformed or missing slashes!")

    # Simulate how it should appear in requirements.txt
    print(f"\nPaste this in requirements.txt as editable:\n-e {abs_path}\n")

if __name__ == "__main__":
    check_project_path()