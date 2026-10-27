# Cómo está organizada la plantilla

```text
api-rest-starter/
├── demo_api.py          # Servicio local de ejemplo
├── tests/
│   ├── conftest.py      # Inicia y detiene el servicio local
│   └── test_api.py      # Casos y datos mínimos del reporte
├── docs/                # Manual que estás leyendo
├── mkdocs.yml           # Navegación, tema y colores
└── pyproject.toml       # Dependencias y configuración de pytest
```

## Lo que ejecutarás normalmente

1. `poetry install` instala las dependencias.
2. `poetry run python -m pytest ...` descubre funciones llamadas `test_*` y ejecuta sus aserciones.
3. `pytest-html` escribe el reporte HTML cuando le pasas `--html`.
4. `poetry run mkdocs serve` muestra este manual durante la edición.

`demo_api.py` existe para que el ejercicio sea repetible. Sus datos son ficticios. En una API real, sustituye las llamadas de ejemplo como indica [Adaptar las pruebas](adaptar.md).

## Qué hace una prueba

```python
def test_consultar_usuario(api_url, extras):
    response = requests.get(f"{api_url}/users/1", timeout=10)
    registrar_http(extras, response)
    assert response.status_code == 200
    assert response.json()["name"] == "Ada Lovelace"
```

- `api_url` apunta al servicio local temporal.
- `requests.get()` envía la petición.
- `response` contiene estado, cuerpo y tiempos.
- `registrar_http()` agrega detalles al HTML.
- Las expresiones `assert` determinan si pasó la prueba.

El reporte y el sitio generado están ignorados por Git; no necesitas guardarlos en el código fuente.
