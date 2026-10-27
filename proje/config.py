import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
INSTANCE_DIR = PROJECT_ROOT / "instance"


class Config:
    SECRET_KEY = os.environ.get("LMS_SECRET_KEY", "dev-only-change-me")

    DATABASE_PATH = Path(
        os.environ.get("LMS_DATABASE_PATH", str(INSTANCE_DIR / "lms_local.db"))
    )

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
