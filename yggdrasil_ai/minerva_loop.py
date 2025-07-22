import os
import sys
import time
import uuid
from pathlib import Path

# Ensure the yggdrasil_ai package is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from yggdrasil_ai.rag import ask_yggdrasil
from memory_manager import create_memory, ingest_memory

GOALS_FILE = "goals.md"
SLEEP_INTERVAL = 3600  # Run every hour

def read_goals(filepath=GOALS_FILE):
    if Path(filepath).exists():
        return Path(filepath).read_text().splitlines()
    return []

def minerva_reflection_loop():
    goals = read_goals()
    for goal in filter(None, map(str.strip, goals)):
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
        ingest_memory(mem)

if __name__ == "__main__":
    while True:
        minerva_reflection_loop()
        time.sleep(SLEEP_INTERVAL)