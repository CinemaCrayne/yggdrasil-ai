import streamlit as st
import pandas as pd
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("yggdrasil-memory")

st.title("🌌 Yggdrasil Memory Constellation")

query = st.text_input("Ask Yggdrasil a question:")
if st.button("Ask"):
    if query:
        response = ask_yggdrasil(query)
        st.write("**Response:**", response)
    else:
        st.warning("Please enter a question.")

query = st.text_input("Search by branch or priority")

results = index.describe_index_stats()
all_items = results.get("namespaces", {}).get("", {}).get("vectors", {})

if query:
    st.warning("Basic filtering not implemented yet. Try embedding-based search in the future!")

# Simulated layout
st.markdown("### 📂 Memory Map")

try:
    # Dummy render
    stats = index.describe_index_stats()
    st.json(stats)
except Exception as e:
    st.error(f"Could not load constellation: {e}")