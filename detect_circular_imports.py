import os

def find_imports(root_dir, target="import app"):
    matches = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(subdir, file)
                with open(path, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f, start=1):
                        if target in line:
                            matches.append((path, i, line.strip()))
    return matches

def main():
    print("🔍 Scanning for circular imports involving `import app`...\n")
    matches = find_imports(".", "import app")
    if matches:
        print("🚨 Potential circular import(s) found:\n")
        for path, line_num, line in matches:
            print(f"{path} [Line {line_num}]: {line}")
        print("\n👉 Consider removing or refactoring these imports.")
    else:
        print("✅ No circular imports found involving `import app`.")

if __name__ == "__main__":
    main()