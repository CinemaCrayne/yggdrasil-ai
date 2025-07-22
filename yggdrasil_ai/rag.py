# yggdrasil_ai/rag.py

import os
import time
import sys
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from datetime import datetime
from typing import List, Dict
from ratelimit import limits, sleep_and_retry
from uuid import uuid4

# === CONFIGURATION ===
load_dotenv()

pinecone_api_key = os.environ.get("PINECONE_API_KEY")
if not pinecone_api_key:
    raise RuntimeError("PINECONE_API_KEY is missing from environment")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# === SANITIZATION ===
def remove_non_ascii(value: str) -> str:
    clean = value.encode("ascii", "ignore").decode()
    if clean != value:
        print(f"[WARN] Removed non-ASCII from env value: '{value}' → '{clean}'", file=sys.stderr)
    return clean

def sanitize_metadata(md: Dict) -> Dict:
    sanitized = {}
    for k, v in md.items():
        original = str(v)
        cleaned = remove_non_ascii(original)
        if original != cleaned:
            print(f"[WARN] Non-ASCII removed from '{k}': '{original}' → '{cleaned}'")
        sanitized[k] = cleaned
    return sanitized

# Sanitize env values before using them
PINECONE_INDEX_NAME = remove_non_ascii(os.getenv("PINECONE_INDEX_NAME", "yggdrasil-memory"))
PINECONE_CLOUD = remove_non_ascii(os.getenv("PINECONE_CLOUD", "aws"))
PINECONE_ENVIRONMENT = remove_non_ascii(os.getenv("PINECONE_ENVIRONMENT", "us-east-1"))

# === INIT PINECONE ===
pc = Pinecone(api_key=pinecone_api_key)
VECTOR_DIM = 1536
EMBED_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o"

# === RATE LIMITS (OpenAI recommendation) ===
MAX_CALLS_PER_MINUTE = 60
MAX_CALLS_PER_SECOND = 3

# === RATE-LIMITED CALLS ===
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_SECOND, period=1)
def rate_limited_embed_call(text: str):
    return client.embeddings.create(
        model=EMBED_MODEL,
        input=[text]
    )

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_SECOND, period=1)
def rate_limited_chat_call(prompt: str):
    return client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

# === ENSURE INDEX EXISTS ===
try:
    existing = pc.list_indexes().names()
    if PINECONE_INDEX_NAME not in existing:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=VECTOR_DIM,
            spec=ServerlessSpec(
                cloud=PINECONE_CLOUD,
                region=PINECONE_ENVIRONMENT
            )
        )
except UnicodeEncodeError as e:
    raise RuntimeError(f"[FATAL] Unicode issue during index check: {e}")

# === CONNECT TO INDEX ===
pinecone_index = pc.Index(name=PINECONE_INDEX_NAME)

# === MEMORY STRUCTURE ===
def format_memory_block(memory: Dict) -> str:
    return f"[{memory['priority']}][{memory['branch']}] Code: {memory['code']} – {memory['notes']}"

def build_prompt(memories: List[Dict], user_query: str) -> str:
    formatted = "\n".join([format_memory_block(m) for m in memories])
    return f"""\nYou are YggdrasilBot, a memory-powered AI. Use the following memories to answer the question.\n\n=== Memory Context ===\n{formatted}\n=== End Context ===\n\nUser's question: {user_query}\nAnswer concisely, citing memory codes where relevant.\n""".strip()

# === EMBEDDING ===
def embed_text(text: str) -> List[float]:
    response = rate_limited_embed_call(text)
    return response.data[0].embedding

def embed_memory_text(text: str) -> List[float]:
    return embed_text(text)

# === INGESTION ===
def add_memory(memory: Dict):
    embedding = embed_text(memory["notes"])
    pine_id = memory["id"]

    metadata = sanitize_metadata({
        "priority": memory["priority"],
        "branch": memory["branch"],
        "code": memory["code"],
        "ai_name": memory.get("ai_name", "YggdrasilBot"),
        "notes": memory["notes"],
        "date_last_updated": memory.get("date_last_updated", datetime.now().isoformat())
    })

    print(f"[DEBUG] Upserting memory with metadata: {metadata}")

    pinecone_index.upsert([
        (pine_id, embedding, metadata)
    ])

def store_memory_vector(content: str, vector: List[float], tags: List[str], memory_type: str, namespace: str = "") -> str:
    memory_id = str(uuid4())
    metadata = sanitize_metadata({
        "content": content,
        "tags": ", ".join(tags),
        "type": memory_type,
        "timestamp": datetime.now().isoformat()
    })

    pinecone_index.upsert([(memory_id, vector, metadata)], namespace=namespace)
    return memory_id

# === RETRIEVAL ===
def retrieve_memories(query: str, top_k: int = 5) -> List[Dict]:
    query_vector = embed_text(query)
    result = pinecone_index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    return [match.metadata or {} for match in result.matches]

def query_memory_vector(vector, namespace="", filter=None, top_k=5):
    from pinecone import Index
    index = Index("your-index-name")  # replace with your actual index name

    query_args = {
        "vector": vector,
        "top_k": top_k,
        "include_metadata": True,
    }

    if namespace:
        query_args["namespace"] = namespace

    if filter:
        query_args["filter"] = filter

    results = index.query(**query_args)
    return results.matches

# === RESPONSE GENERATION ===
def ask_yggdrasil(query: str) -> str:
    retrieved = retrieve_memories(query)
    prompt = build_prompt(retrieved, query)
    response = rate_limited_chat_call(prompt)
    return response.choices[0].message.content.strip()