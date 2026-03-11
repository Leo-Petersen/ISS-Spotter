#!/usr/bin/env python3
"""Flask server that serves the ISS dashboard."""

import json
import os

from flask import Flask, render_template, jsonify

app = Flask(__name__)

DATA_DIR = "/opt/iss-spotter/data"

def read_json(filename):
    """Safely read a JSON file and return its contents."""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

@app.route("/")
def index():
    """Serve the dashboard page."""
    position = read_json("iss_position.json")
    return render_template("index.html", position=position)

@app.route("/api/position")
def api_position():
    """JSON endpoint, returns the latest ISS position."""
    position = read_json("iss_position.json")
    if position is None:
        return jsonify({"error": "No data yet"}), 404
    return jsonify(position)

@app.route("/api/history")
def api_history():
    """JSON endpoint, returns position history for the trail."""
    history = read_json("iss_history.json")
    if history is None:
        return jsonify([])
    return jsonify(history)

@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)