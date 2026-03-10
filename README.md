# ISS Spotter

## Live Site
https://iss-spotter.149.165.170.56.nip.io/

## Overview
A live dashboard that tracks the current location of the International Space Station (ISS) on an interactive 3D globe. A background script fetches position data every 5 minutes, and a Flask web server displays the latest coordinates, timestamp, and orbital trail.

## How It Works
- A Python script runs every 5 minutes via a `systemd` timer. It calls the Open Notify API (`http://api.open-notify.org/iss-now.json`) and writes the latitude, longitude, and timestamp to a JSON file. It also maintains a history of the last 100 data points.
- A Flask web server reads those files and serves a dashboard with a 3D globe (using Globe.gl) showing the ISS position and its recent path.
- Caddy handles HTTPS and routes requests to the Flask app using a custom `.nip.io` subdomain.

## Technologies
- **Language:** Python
- **Web Framework:** Flask + Gunicorn
- **3D Globe:** Globe.gl (Three.js-based)
- **Scheduling:** `systemd` timer
- **Data Source:** Open Notify API (no API key required)
- **Web Server & SSL:** Caddy (automatic Let's Encrypt)
- **CI/CD:** GitHub Actions (auto-deploy on push to `main`)
- **Firewall:** Jetstream2 security group, only ports 22, 80, 443 open

## Architecture
```
systemd timer (every 5 min)
    -> fetch_iss.py -> writes JSON to /opt/iss-spotter/data/

Browser -> Caddy (HTTPS) -> Gunicorn/Flask (port 5000) -> reads JSON -> serves dashboard
```