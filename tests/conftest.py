"""Levanta y detiene una API local por ejecución; sin procesos manuales."""

from threading import Thread
from http.server import ThreadingHTTPServer

import pytest

from demo_api import DemoAPI


@pytest.fixture(scope="session")
def api_url():
    server = ThreadingHTTPServer(("127.0.0.1", 0), DemoAPI)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
