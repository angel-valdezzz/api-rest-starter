"""API local de aprendizaje; se inicia sola al ejecutar pytest."""

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


class DemoAPI(BaseHTTPRequestHandler):
    def _send(self, status: int, body: dict) -> None:
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self) -> None:
        if self.path == "/users/1":
            self._send(200, {"id": 1, "name": "Ada Lovelace"})
        elif self.path.startswith("/users/"):
            self._send(404, {"error": "Usuario no encontrado"})
        else:
            self._send(404, {"error": "Ruta no encontrada"})

    def do_POST(self) -> None:
        size = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(size)

        if self.path == "/users":
            try:
                data = json.loads(body)
            except (json.JSONDecodeError, UnicodeDecodeError):
                self._send(400, {"error": "JSON inválido"})
                return
            if not isinstance(data, dict) or not data.get("name"):
                self._send(400, {"error": "El nombre es obligatorio"})
                return
            self._send(201, {"id": 2, "name": data["name"]})
        elif self.path == "/echo-form":
            if self.headers.get_content_type() != "application/x-www-form-urlencoded":
                self._send(415, {"error": "Se esperaba un formulario"})
                return
            values = parse_qs(body.decode("utf-8"), keep_blank_values=True)
            self._send(200, {key: items[0] for key, items in values.items()})
        else:
            self._send(404, {"error": "Ruta no encontrada"})
