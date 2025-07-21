import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rag.py import ask_yggdrasil
import time
from pathlib import Path
from rag.py import ask_yggdrasil
from memory_manager import create_memory
import uuid

def read_goals(filepath="goals.md"):
    if Path(filepath).exists():
        return Path(filepath).read_text().splitlines()
    return []

def minerva_reflection_loop():
    goals = read_goals()
    for goal in goals:
        if goal.strip():
            print(f"[OK] Reflecting on goal: {goal}")
            response = ask_yggdrasil(goal)
            print(f"[OK] Response: {response}")
            mem = create_memory(
                id=str(uuid.uuid4()),
                code=f"reflection_{uuid.uuid4().hex[:6]}",
                notes=response,
                priority="2",
                branch="reflections"
            )
            from memory_manager import ingest_memory
            ingest_memory(mem)

if __name__ == "__main__":
    while True:
        minerva_reflection_loop()
        time.sleep(3600)  # Run every hour