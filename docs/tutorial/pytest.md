# Escribir pruebas con pytest

Una función cuyo nombre comienza por `test_` representa un caso. Su nombre debe explicar el comportamiento, por ejemplo `test_nombre_obligatorio`.

```python
def test_nombre_obligatorio(api_url, extras):
    response = requests.post(f"{api_url}/users", json={}, timeout=10)
    registrar_http(extras, response)

    assert response.status_code == 400
    assert response.json()["error"] == "El nombre es obligatorio"
```

## Preparar, actuar, comprobar

1. **Preparar:** define URL y datos de entrada.
2. **Actuar:** envía la petición con `requests`.
3. **Comprobar:** usa `assert` para validar código y contenido.

`api_url` es una **fixture**: pytest ejecuta su función de `tests/conftest.py` y entrega su resultado a las pruebas que la piden. Así todas usan la misma API de ejemplo durante la ejecución sin iniciarla a mano. `extras` lo aporta `pytest-html` para adjuntar el intercambio al reporte.

## Elegir qué ejecutar

```bash
poetry run python -m pytest -v
poetry run python -m pytest tests/test_api.py::test_nombre_obligatorio -v
poetry run python -m pytest -k usuario -v
```

Si una aserción falla, pytest muestra **qué valor observó** y cuál esperaba. En el HTML, abre el caso fallido para consultar la respuesta registrada.

!!! tip "La prueba del error también debe pasar"
    El caso `test_nombre_obligatorio` espera `400`. Si llega `400` y el mensaje coincide, el caso está aprobado.
