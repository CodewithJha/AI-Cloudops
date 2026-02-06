AI CloudOps
===========

AI CloudOps is a modular Python project that turns the original “all-in-one script in README” into a clean, runnable app with:
- A **Web Dashboard** (FastAPI) for a modern UI
- A **Desktop GUI** (Tkinter) for a local desktop experience
- A **modular codebase** where each feature lives in its own file

This repo is designed to be **safe for GitHub**: configuration is read from a local `.env` file (not committed).

What’s inside (features)
------------------------

Web dashboard (`server.py`)
- **Camera preview** (browser permission) + basic filters
- **Location lookup**: search by address/city
- **Live device location**: request device permission and reverse-geocode to city/address
- **Email sending** via SMTP (recommended: Mailtrap sandbox for testing)
- **AWS EC2 actions**: start/stop/terminate (requires AWS credentials)
- **AWS S3 actions**: upload/delete (requires AWS credentials)
- **Activity feed**: shows recent actions in the UI

Desktop GUI (`main.py`)
- **Camera filters** (OpenCV window)
- **Location lookup** (dialog input)
- **Email sending** (dialogs)
- **EC2 start/stop/terminate**
- **S3 upload/delete**
- **Open webpage**

Screenshots / Demo
------------------
- Demo page: `docs/DEMO.md`

Add your screenshots to `docs/screenshots/` as:
- `01-dashboard-top.png`
- `02-core-cards.png`
- `03-aws-and-activity.png`

They will render automatically on GitHub in `docs/DEMO.md`.

Important note about “public deployment”
----------------------------------------
If you deploy this publicly, features like **EC2/S3 actions** must be protected with:
- Authentication (login)
- Authorization (roles)
- Audit logs
- Confirmations / safe-guards

For GitHub / portfolio use, keep AWS credentials local and consider running in “demo-only” mode (no real cloud actions) for public demos.

Tech stack
----------
- **Python**: 3.10+
- **Web**: FastAPI + Uvicorn
- **Desktop**: Tkinter
- **AWS**: boto3
- **Camera**: OpenCV
- **Geo**: geopy (Nominatim)

Project structure
-----------------
```
AI-CloudOps/
  ai_cloudops/
    __init__.py
    config.py          # reads .env
    camera.py          # OpenCV camera filters
    geolocation.py     # forward geocoding
    emailer.py         # SMTP email sending
    aws_ec2.py         # EC2 start/stop/terminate
    aws_s3.py          # S3 upload/delete
    web.py             # open webpage helper
    gui.py             # Tkinter UI wiring
  main.py              # desktop entrypoint
  server.py            # web entrypoint
  requirements.txt
  env.example          # template for local .env (do not commit real secrets)
  .gitignore
  README.md
```

Setup (Windows PowerShell)
--------------------------
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item env.example .env
```

Run locally
-----------

Web dashboard
```
.\.venv\Scripts\python.exe -m uvicorn server:app --host 127.0.0.1 --port 8001 --reload
```
Open:
- http://127.0.0.1:8001

Desktop GUI
```
.\.venv\Scripts\python.exe main.py
```

Configuration (.env)
--------------------
Copy `env.example` → `.env` and fill only what you need.

Email (SMTP)
- SMTP_HOST
- SMTP_PORT
- SMTP_USERNAME
- SMTP_PASSWORD
- SMTP_FROM

Recommended for testing email: Mailtrap (Email Testing inbox)
- Your emails will appear in Mailtrap, not in a real inbox.

AWS
- AWS_REGION (example: `ap-south-1`)
- Prefer `AWS_PROFILE` (AWS CLI profile / SSO), otherwise use:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - AWS_SESSION_TOKEN (optional)
- S3_DEFAULT_BUCKET (default bucket used by the UI)

App
- DEFAULT_WEB_URL (used by “Open Web Page” in desktop GUI)
- APP_TITLE (desktop window title)

Security checklist (before pushing to GitHub)
---------------------------------------------
- Never commit `.env` (this repo ignores it).
- Never paste SMTP/AWS secrets into code/README.
- If any key was ever exposed, **rotate it** in the provider dashboard.
- Use least-privilege AWS IAM permissions.

Troubleshooting
---------------

Web UI doesn’t change after edits
- Hard refresh browser: `Ctrl + F5`
- Ensure you’re on the correct port (example: `8001`)

Live location doesn’t work
- Browser must grant location permission
- Check Windows location settings
- Try Chrome/Edge

Camera issues
- Ensure no other app is using the camera
- Browser must grant camera permission

AWS errors
- Verify region/profile and run: `aws sts get-caller-identity`

Geocoding rate limits
- Nominatim can rate limit; try again later

License
-------
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

Contributing / Forking
----------------------
- This repo is primarily a portfolio / learning project.
- You are welcome to **fork** it and adapt it to your own cloud environment.
- If you open a PR, please avoid adding real credentials or cloud account details.

