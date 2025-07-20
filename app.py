from flask import Flask, request, jsonify, send_file, send_from_directory
from yggdrasil_ai.rag import add_memory, ask_yggdrasil
from uuid import uuid4
from flask_cors import CORS

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

# New route to handle Custom GPT Action calls
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
            message = f"Avasrota invoked to preserve memory of: {forgotten}"
        case _:
            return jsonify({"error": "Unknown voice"}), 400

    return jsonify({"message": message})

# Local dev server (disabled in production)
if __name__ == "__main__":
    import os
    if os.environ.get("FLASK_ENV") != "production":
        app.run(debug=True, port=5000)
