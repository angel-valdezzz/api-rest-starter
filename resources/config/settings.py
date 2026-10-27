"""Execution settings. Credentials are never included in the settings representation."""

from dataclasses import dataclass, field
from os import environ
from urllib.parse import urlparse


@dataclass(frozen=True)
class ApiSettings:
    base_url: str
    api_key: str = field(repr=False)
    timeout: float = 15.0

    def __post_init__(self):
        if urlparse(self.base_url).scheme not in {"http", "https"}:
            raise ValueError("DEMO_BASE_URL must be an HTTP(S) URL")
        if not self.api_key:
            raise ValueError("DEMO_API_KEY is required")
        if self.timeout <= 0:
            raise ValueError("HTTP timeout must be positive")

    @classmethod
    def from_environment(cls):
        return cls(
            base_url=environ.get("DEMO_BASE_URL", "").rstrip("/"),
            api_key=environ.get("DEMO_API_KEY", ""),
            timeout=float(environ.get("HTTP_TIMEOUT", "15")),
        )
