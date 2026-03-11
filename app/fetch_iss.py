#!/usr/bin/env python3
"""Fetch ISS position and write to a JSON file."""

import json
import os
import sys
from datetime import datetime, timezone

import requests

# Where the data lives, use an absolute path so systemd can find it
DATA_DIR = "/opt/iss-spotter/data"
DATA_FILE = os.path.join(DATA_DIR, "iss_position.json")

def fetch_iss_position():
    """Call the Open Notify API and return position dictionary"""
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    return {
        "latitude": float(data["iss_position"]["latitude"]),
        "longitude": float(data["iss_position"]["longitude"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "unix_timestamp": data["timestamp"],
    }

def save_position(position):
    """Write position to JSON file. Also append to history."""
    os.makedirs(DATA_DIR, exist_ok=True)

    # Write the latest position (Flask reads this)
    with open(DATA_FILE, "w") as f:
        json.dump(position, f, indent=2)

    # Append to a history file (keeps the last 100 entries for the map trail)
    history_file = os.path.join(DATA_DIR, "iss_history.json")
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.append(position)
    history = history[-90:]  # keep last 90 data points (The ISS takes roughly 90 minutes to orbit around the earth, ~16 times per 24 hours)

    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

def main():
    try:
        position = fetch_iss_position()
        save_position(position)
        print(f"[OK] ISS at {position['latitude']}, {position['longitude']}")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()