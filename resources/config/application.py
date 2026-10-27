"""Optional lifecycle of the actual installed Demo Users API; no endpoints are implemented here."""

import json
import os
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from contextlib import contextmanager

from resources.config.settings import ApiSettings


@contextmanager
def local_application():
    key = secrets.token_urlsafe(40)
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    settings = ApiSettings(f"http://127.0.0.1:{port}", key)
    # Run outside the repository so historical starter modules cannot shadow the installed package.
    with tempfile.TemporaryDirectory(prefix="demo-users-api-") as directory:
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "demo_api.main:create_app",
                "--factory",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
                "--no-access-log",
                "--log-level",
                "warning",
            ],
            cwd=directory,
            env={**os.environ, "API_KEYS": json.dumps({"automation": key})},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            deadline = time.monotonic() + 30
            while True:
                if process.poll() is not None:
                    raise RuntimeError("The installed Demo Users API exited during startup")
                try:
                    with urllib.request.urlopen(
                        settings.base_url + "/health", timeout=1
                    ) as response:
                        if json.load(response) == {"status": "ok", "storage": "temporary"}:
                            break
                except (OSError, ValueError):
                    pass
                if time.monotonic() >= deadline:
                    raise RuntimeError("Demo Users API did not become healthy within 30 seconds")
                time.sleep(0.1)
            yield settings
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
