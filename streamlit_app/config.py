"""Streamlit configuration sourced from environment variables."""

import os


BACKEND_URL = os.getenv("ATMOSYNC_BACKEND_URL", "http://127.0.0.1:8000/api/v1").rstrip("/")
REQUEST_TIMEOUT = float(os.getenv("ATMOSYNC_REQUEST_TIMEOUT", "8"))
