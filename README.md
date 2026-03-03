# ISS Spotter

**Track:** C – The Observer (Automated Data Pipeline)

## Overview
I'm building a live dashboard that tracks the current location of the International Space Station (ISS). The app will have two parts: a background script that fetches position data every few minutes, and a simple web page that displays the latest coordinates and timestamp. (potentially on a globe/map?)

## How It Works
- A Python script runs every 5 minutes via a `systemd` timer. It calls the Open Notify API (`http://api.open-notify.org/iss-now.json`) and writes the latitude, longitude, and timestamp to a JSON file.
- A Flask web server reads that file and serves a minimal HTML page showing the current ISS position and when it was last updated.
- Caddy will handle HTTPS and route requests to the Flask app using a custom `*.nip.io` subdomain (e.g., `iss-spotter.<my-ip>.nip.io`).

## Technologies
- **Language:** Python
- **Web Framework:** Flask (may potentially use Django instead, I have experience with that from another class)
- **Scheduling:** `systemd` timer
- **Data Source:** Open Notify API (no API key required)
- **Web Server & SSL:** Caddy (automatic Let's Encrypt)
- **CI/CD:** GitHub Actions (auto‑deploy on push to `main`)
- **Firewall:** Jetstream2 security group, only ports 22, 80, 443 open

## Why This Meets the Requirements
- **Least privilege:** Only necessary ports are open.
- **GitOps:** Deployment is fully automated via GitHub Actions.
- **Multi‑tenant routing & SSL:** Caddy provides HTTPS on a `.nip.io` domain.
- **Resilience:** Both the Flask app and the background timer are managed by `systemd`, they will restart automatically if the instance reboots.
- **Track C:** Automated data pipeline with a separate scheduled task.