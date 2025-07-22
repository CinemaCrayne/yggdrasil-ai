from flask import Flask, request, jsonify, send_file, send_from_directory
from yggdrasil_ai.rag import add_memory, ask_yggdrasil, embed_memory_text, store_memory_vector, query_memory_vector
from uuid import uuid4
from flask_cors import CORS
import openai  # ensure you have access set via environment or config

app = Flask(__name__)
CORS(app)

@app.route("/.well-known/ai-plugin.json")
def plugin_manifest():
    return send_from_directory(".well-known", "ai-plugin.json")

@app.route("/openapi.yaml")
def serve_openapi_spec():
    return send_file("openapi.yaml", mimetype="text/yaml")

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Yggdrasil is active"}), 200

@app.route("/add_memory", methods=["POST"])
def add_memory_endpoint():
    data = request.get_json()
    memory = {
        "id": str(uuid4()),
        "priority": data["priority"],
        "branch": data["branch"],
        "code": data["code"],
        "notes": data["notes"],
        "ai_name": data.get("ai_name", "YggdrasilBot")
    }
    add_memory(memory)
    return jsonify({"message": "Memory added."}), 201

@app.route("/ask", methods=["POST"])
def ask():
    query = request.json.get("query")
    if not query:
        return jsonify({"error": "Missing 'query' field"}), 400
    answer = ask_yggdrasil(query)
    return jsonify({"response": answer})

@app.route("/invoke", methods=["POST"])
def invoke_voice():
    data = request.get_json()
    voice = data.get("voice")

    match voice:
        case "aegis_guardian":
            context = data.get("context", "")
            message = f"Aegis invoked to defend moral truth in: {context}"
        case "maitreya_empath":
            grief = data.get("grief_source", "")
            message = f"Maitreya invoked to heal sorrow from: {grief}"
        case "samanvaya_mediator":
            conflict = data.get("conflict", "")
            message = f"Samanvaya invoked to reconcile: {conflict}"
        case "siddhartha_conscience":
            decision = data.get("decision_point", "")
            message = f"Siddhartha invoked to guide decision: {decision}"
        case "unchained_witness":
            injustice = data.get("injustice", "")
            message = f"Unchained One invoked to expose: {injustice}"
        case "avasrota_memory":
    forgotten = data.get("forgotten", "")
    context = data.get("context", "")
    content = context if context else forgotten

    try:
        if content:
            tags = generate_tags(f"Extract tags for memory: {content}")
            vector = embed_memory_text(content)
            store_memory_vector(content, vector, tags, "insight", namespace="user_001")
            message = f"Avasrota invoked to preserve memory of: {forgotten or context}"
        else:
            message = "Avasrota invoked, but no memory content was provided."
    except Exception as e:
        message = f"Avasrota failed to store memory due to: {str(e)}"
        case _:
            return jsonify({"error": "Unknown voice"}), 400

    return jsonify({"message": message})

def generate_tags(prompt: str) -> list:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Extract 5–7 concise tags as lowercase keywords from the following content."},
            {"role": "user", "content": prompt}
        ]
    )
    tags_str = response['choices'][0]['message']['content']
    return [tag.strip().lower() for tag in tags_str.split(",") if tag.strip()]

@app.route("/memory/store", methods=["POST"])
def store_memory():
    data = request.get_json()
    content = data.get("content")
    tags = data.get("tags", [])
    memory_type = data.get("type", "note")
    namespace = data.get("namespace", "")  # optional

    if not content:
        return jsonify({"error": "Missing content field"}), 400

    if not tags:
        tags = generate_tags(f"Extract tags for memory: {content}")

    vector = embed_memory_text(content)
    result = store_memory_vector(content, vector, tags, memory_type, namespace=namespace)

    return jsonify({"status": "stored", "id": result}), 200

@app.route("/memory/query", methods=["POST"])
def query_memory():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing query field"}), 400

    vector = embed_memory_text(query)
    results = query_memory_vector(vector)

    filtered = []
    for r in results:
        metadata = r.get("metadata") or {}
        score = r.get("score", 0)
        if isinstance(metadata, dict) and isinstance(score, (int, float)):
            filtered.append({"score": score, "metadata": metadata})

    return jsonify({"matches": filtered}), 200

@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "Yggdrasil AI API is running"}), 200

if __name__ == "__main__":
    import os
    if os.environ.get("FLASK_ENV") != "production":
        app.run(debug=True, port=5000)