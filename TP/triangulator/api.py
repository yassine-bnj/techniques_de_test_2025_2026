from flask import Flask, request, send_file
from .core import decode_pointset, triangulate, encode_triangles
import io

app = Flask(__name__)

@app.route("/triangulate", methods=["POST"])
def triangulate_endpoint():
    """Endpoint principal du Triangulator."""
    raise NotImplementedError