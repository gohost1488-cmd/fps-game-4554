"""AHVE FPS Server — fps-game-4554."""
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
players = {}
queue = []
matches = {}

@app.route("/health")
def health():
    return jsonify({"status":"ok","game":"fps-game-4554"})

@app.route("/register", methods=["POST"])
def register():
    d = request.get_json()
    pid = d.get("player_id", str(uuid.uuid4())[:8])
    players[pid] = {"name": d.get("name",pid), "mmr":1000}
    return jsonify({"player_id":pid})

@app.route("/match/join", methods=["POST"])
def join():
    pid = request.get_json()["player_id"]
    queue.append(pid)
    if len(queue) >= 10:
        mid = str(uuid.uuid4())[:8]
        matches[mid] = {"players":queue[:10], "status":"active"}
        queue.clear()
        return jsonify({"match_id":mid})
    return jsonify({"status":"queued"})

@app.route("/rating/update", methods=["POST"])
def rating():
    d = request.get_json()
    pid = d["player_id"]
    if pid in players:
        players[pid]["mmr"] += 25
    return jsonify({"mmr":players[pid]["mmr"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
