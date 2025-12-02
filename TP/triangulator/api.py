from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/triangulate/<pointset_id>", methods=["GET"])
def triangulate_route(pointset_id):
    """Endpoint principal de triangulation (placeholder)."""
    return jsonify({"error": "Not implemented"}), 501
