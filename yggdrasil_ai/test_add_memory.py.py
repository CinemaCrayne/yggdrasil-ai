from yggdrasil_ai.rag import add_memory
from uuid import uuid4

test_memory = {
    "id": str(uuid4()),
    "priority": "High",
    "branch": "Reflection",
    "code": "R001",
    "notes": "Yggdrasil stores and retrieves memory for AI reasoning.",
    "ai_name": "YggdrasilBot"
}

add_memory(test_memory)
print("✅ Test memory added to Pinecone.")