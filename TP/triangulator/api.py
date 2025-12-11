"""Flask API for the Triangulator microservice."""

import io

import requests
from flask import Flask, jsonify, request, send_file

from .core import decode_pointset, encode_triangles, triangulate

app = Flask(__name__)


@app.route("/triangulate", methods=["POST"])
def triangulate_endpoint():
    """Handle triangulation requests from clients.

    Expects a JSON payload with a 'pointSetId' field.
    Fetches the corresponding PointSet from the PointSetManager,
    computes the triangulation, and returns the result as binary data.

    Returns:
        HTTP 200 with binary Triangles data on success.
        HTTP 400 for invalid input.
        HTTP 404 if PointSet not found.
        HTTP 502 if PointSetManager is unreachable or returns an error.
        HTTP 500 for data decoding or triangulation errors.

    """
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    if not data or "pointSetId" not in data:
        return jsonify({"error": "Missing 'pointSetId'"}), 400

    point_set_id = data["pointSetId"]
    if not isinstance(point_set_id, int) or point_set_id < 0:
        return jsonify({"error": "'pointSetId' must be a non-negative integer"}), 400

    # Fetch PointSet from PointSetManager
    try:
        url = f"http://localhost:5000/pointsets/{point_set_id}"
        response = requests.get(url, timeout=5)
    except requests.RequestException:
        return jsonify({"error": "PointSetManager unreachable"}), 502

    if response.status_code == 404:
        return jsonify({"error": "PointSet not found"}), 404
    elif response.status_code != 200:
        return jsonify({"error": "PointSetManager error"}), 502

    # Process triangulation
    try:
        points = decode_pointset(response.content)
        triangles_indices = triangulate(points)
        result_binary = encode_triangles(points, triangles_indices)
    except ValueError as e:
        return jsonify({"error": f"Invalid data: {str(e)}"}), 500

    return send_file(
        io.BytesIO(result_binary),
        mimetype="application/octet-stream"
    )