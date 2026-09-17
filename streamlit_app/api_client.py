"""Small HTTP client for the AtmoSync API."""

from typing import Any, Dict, Optional

import httpx

from .config import BACKEND_URL, REQUEST_TIMEOUT


class ApiError(RuntimeError):
    """Raised when the backend cannot provide a valid response."""


class ApiClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        headers: Dict[str, str] = kwargs.pop("headers", {})
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            response = httpx.request(
                method,
                f"{BACKEND_URL}/{path.lstrip('/')}",
                headers=headers,
                timeout=REQUEST_TIMEOUT,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, ValueError) as exc:
            detail = "Backend unavailable"
            if isinstance(exc, httpx.HTTPStatusError):
                detail = f"Backend returned HTTP {exc.response.status_code}"
                try:
                    detail = str(exc.response.json().get("detail", detail))
                except ValueError:
                    pass
            elif isinstance(exc, httpx.ConnectError):
                detail = f"Backend unavailable at {BACKEND_URL}. Start FastAPI on 127.0.0.1:8000."
            elif isinstance(exc, httpx.TimeoutException):
                detail = f"Backend request timed out after {REQUEST_TIMEOUT:g}s at {BACKEND_URL}."
            raise ApiError(detail) from exc

    def get(self, path: str, **params: Any) -> Any:
        return self.request("GET", path, params=params)

    def post_file(self, path: str, file_name: str, content: bytes) -> Any:
        return self.request("POST", path, files={"file": (file_name, content)})
