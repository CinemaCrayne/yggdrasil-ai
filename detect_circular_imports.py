import os

def find_imports(root_dir, target="import app"):
    matches = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f, start=1):
                            if target in line:
                                matches.append((path, i, line.strip()))
                except (UnicodeDecodeError, FileNotFoundError):
                    continue
    return matches

if __name__ == "__main__":
    print("Scanning for circular imports involving `import app`...\n")
    matches = find_imports(".", "import app")
    if matches:
        for path, line_num, line in matches:
            print(f"{path} [Line {line_num}]: {line}")
        print("\nConsider refactoring these imports if circular dependency is suspected.")
    else:
        print("No circular imports found involving `import app`.")