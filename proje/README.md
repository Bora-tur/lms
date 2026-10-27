# LMS — Library Monitoring System

A course-project prototype that simulates library entry/exit using QR codes and
publishes only aggregate occupancy information to a separate public service.

## Current status

This starter contains the initial local Flask app and a health-check endpoint.
Database initialization, authentication, QR validation, gate events, frontend
camera scanning, and the separate public service will be added incrementally.

## Requirements

- Python 3.10 or newer recommended
- Git
- macOS or Windows

## macOS setup

From this folder, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000/health. Expected response:

```json
{
  "service": "lms-local",
  "status": "ok"
}
```

## Windows setup

From PowerShell in this folder, run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, use Command Prompt and run
`.venv\Scripts\activate.bat` instead.

## Project scope

- Local service: accounts, QR tokens, entry/exit events, visits, and occupancy calculation.
- Public service: separate database containing aggregate occupancy snapshots only.
- QR reader: browser camera simulation; no physical turnstile hardware.
- Out of scope for the first release: Wi-Fi presence tracking, seat/outlet occupancy,
  SMS notifications, and real hardware integration.

## Important

The built-in Flask server and `debug=True` are for local development only.
Do not expose this development server directly to the public internet.
