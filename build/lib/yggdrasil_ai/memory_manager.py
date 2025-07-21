from datetime import datetime
from yggdrasil_ai.rag import add_memory

def create_memory(id, code, notes, priority, branch, ai_name="YggdrasilBot"):
    return {
        "id": id,
        "code": code,
        "notes": notes,
        "priority": priority,
        "branch": branch,
        "ai_name": ai_name,
        "date_last_updated": datetime.now().isoformat()
    }

def update_memory(existing, updates):
    existing.update(updates)
    existing["date_last_updated"] = datetime.now().isoformat()
    return existing

def prune_memory(memories, priority_threshold=1):
    return [m for m in memories if int(m["priority"]) > priority_threshold]

def summarize_memories(memories):
    return "\n".join([f"[{m['priority']}] {m['code']}: {m['notes']}" for m in memories])

def ingest_memory(memory):
    add_memory(memory)
