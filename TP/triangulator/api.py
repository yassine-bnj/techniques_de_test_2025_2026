from flask import Flask, request, send_file, jsonify
import requests
import io
from .core import decode_pointset, triangulate, encode_triangles

app = Flask(__name__)

@app.route("/triangulate", methods=["POST"])
def triangulate_endpoint():
    # Vérifier le JSON
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    if not data or 'pointSetId' not in data:
        return jsonify({"error": "Missing 'pointSetId'"}), 400

    point_set_id = data['pointSetId']
    if not isinstance(point_set_id, int) or point_set_id < 0:
        return jsonify({"error": "'pointSetId' must be a non-negative integer"}), 400

    # Appeler le PointSetManager
    try:
        response = requests.get(f"http://localhost:5000/pointsets/{point_set_id}", timeout=5)
    except requests.RequestException:
        return jsonify({"error": "PointSetManager unreachable"}), 502

    if response.status_code == 404:
        return jsonify({"error": "PointSet not found"}), 404
    elif response.status_code != 200:
        return jsonify({"error": "PointSetManager error"}), 502

    # Décoder, trianguler, encoder
    try:
        points = decode_pointset(response.content)
        triangles_indices = triangulate(points)
        result_binary = encode_triangles(points, triangles_indices)
    except ValueError as e:
        return jsonify({"error": f"Invalid data: {str(e)}"}), 500

    # Retourner le binaire
    return send_file(
        io.BytesIO(result_binary),
        mimetype='application/octet-stream'
    )