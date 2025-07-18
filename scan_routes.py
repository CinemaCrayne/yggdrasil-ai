import os
import re

project_root = "./yggdrasil_ai"  # adjust if needed
route_pattern = re.compile(r'@app\.route\((.*?)\)', re.DOTALL)

print("📍 Scanning for @app.route(...) definitions...\n")

for dirpath, _, filenames in os.walk(project_root):
    for filename in filenames:
        if filename.endswith(".py"):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = route_pattern.findall(content)
                    if matches:
                        print(f"🧩 {filepath}")
                        for match in matches:
                            print(f"   → @app.route({match.strip()})")
            except Exception as e:
                print(f"❌ Could not read {filepath}: {e}")