import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load your environment variables from .env
load_dotenv()

# Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "yggdrasil-memory")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
VECTOR_DIM = 1536  # for text-embedding-3-small

# Connect to Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check and create index if needed
def ensure_index_exists():
    index_list = pc.list_indexes().names()
    if PINECONE_INDEX_NAME not in index_list:
        print(f"[INFO] Creating index: {PINECONE_INDEX_NAME}")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=VECTOR_DIM,
            spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_ENVIRONMENT),
        )
        print("[OK] Pinecone index created.")
    else:
        print(f"[OK] Pinecone index '{PINECONE_INDEX_NAME}' already exists.")

if __name__ == "__main__":
    ensure_index_exists()