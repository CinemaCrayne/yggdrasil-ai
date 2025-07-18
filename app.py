# app.py
from flask import Flask, request, jsonify
from yggdrasil_ai.rag import add_memory, ask_yggdrasil
from uuid import uuid4

app = Flask(__name__)

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Yggdrasil is active"}), 200

@app.route("/add_memory", methods=["POST"])
def add():
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
    answer = ask_yggdrasil(query)
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

@app.route("/add_memory", methods=["POST"])
def add():
    data = request.get_json()

    required_fields = ["priority", "branch", "code", "notes"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

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
