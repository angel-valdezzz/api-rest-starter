"""Ejemplos de GET, POST JSON, formulario y respuesta de error."""

import pytest_html
import requests


def registrar_http(extras, response):
    """Agrega el intercambio mínimo al detalle de la prueba en el HTML."""
    request = response.request
    request_body = request.body or "(vacío)"
    if isinstance(request_body, bytes):
        request_body = request_body.decode("utf-8", errors="replace")

    extras.append(pytest_html.extras.text(
        f"{request.method} {request.url}\n"
        f"Cuerpo enviado: {str(request_body)[:1000]}\n"
        f"Estado recibido: {response.status_code}\n"
        f"Tiempo HTTP: {response.elapsed.total_seconds():.3f} s\n"
        f"Respuesta: {response.text[:2000]}",
        name="Petición y respuesta",
    ))


def test_consultar_usuario(api_url, extras):
    response = requests.get(f"{api_url}/users/1", timeout=10)
    registrar_http(extras, response)

    assert response.status_code == 200
    assert response.json()["name"] == "Ada Lovelace"


def test_usuario_inexistente(api_url, extras):
    response = requests.get(f"{api_url}/users/999", timeout=10)
    registrar_http(extras, response)

    assert response.status_code == 404
    assert response.json()["error"] == "Usuario no encontrado"


def test_crear_usuario_con_json(api_url, extras):
    response = requests.post(
        f"{api_url}/users", json={"name": "Angel"}, timeout=10
    )
    registrar_http(extras, response)

    assert response.status_code == 201
    assert response.json()["name"] == "Angel"


def test_nombre_obligatorio(api_url, extras):
    response = requests.post(f"{api_url}/users", json={}, timeout=10)
    registrar_http(extras, response)

    assert response.status_code == 400
    assert response.json()["error"] == "El nombre es obligatorio"


def test_enviar_formulario(api_url, extras):
    response = requests.post(
        f"{api_url}/echo-form", data={"nombre": "Angel", "rol": "QA"}, timeout=10
    )
    registrar_http(extras, response)

    assert response.status_code == 200
    assert response.json() == {"nombre": "Angel", "rol": "QA"}
