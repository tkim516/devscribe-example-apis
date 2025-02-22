from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/users", methods=["GET"])
def get_users():
    """Return a list of users."""
    return jsonify([{"id": 1, "name": "Alice"}])

@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    name = request.json.get("name", "New User")
    return jsonify({"id": 2, "name": name})