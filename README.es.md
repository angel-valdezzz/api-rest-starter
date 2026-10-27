# Python · pytest · Requests — Demo Users API

[English](README.md)

Se aplica la arquitectura del ejemplo Robot API: **escenarios, servicios HTTP, assertions de negocio,
configuración y datos/payloads separados**. Las pruebas usan exclusivamente el proyecto real Demo Users API.

## Instalación y ejecución

Python 3.12–3.14 y Poetry 2.5.1, desde la raíz:

```powershell
poetry sync
poetry run pytest --local-api --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
```

Poetry fija el cliente, las herramientas y el proyecto FastAPI independiente por commit.
El arranque y cierre local están en configuración; este repositorio no implementa endpoints HTTP.
Para una API desplegada, configura DEMO_BASE_URL y DEMO_API_KEY en tu terminal y omite --local-api.
Usa una credencial exclusiva de pruebas; .env.example no se carga automáticamente.

```powershell
poetry run pytest -m "not integration"
poetry run pytest --local-api -m integration
poetry run ruff check resources tests
poetry run ruff format --check resources tests
```

## Capas

- tests/test_user_*.py: escenarios completos que componen servicios y comprobaciones semánticas.
- resources/services: peticiones, endpoints y registro/limpieza de IDs propios del caso.
- resources/assertions: códigos HTTP y resultados de negocio; no envían requests.
- resources/config: settings, fixtures, sesiones, aplicación real opcional y carga de entradas.
- data/tables y data/test: escenarios, entradas y resultados esperados.
- data/payloads: plantillas JSON válidas, copiadas y preparadas para cada caso.

Los tests no construyen payloads ni acceden a requests. Los servicios no leen archivos.
Se conservan booleanos y null como tipos JSON. Cada caso prepara correos únicos y limpia sus usuarios
en teardown. Un fallo de limpieza se comunica; no se borra información ajena.
La representación de settings oculta la clave y los logs HTTP no incluyen headers.

Resultados nativos: reports/junit.xml y reports/report.html.
Las restricciones de importación se comprueban en tests/test_architecture.py.

[Arquitectura](docs/architecture.md) · [Escenarios](docs/scenarios.md) · [Validación](VALIDATION.md).
El material anterior con servidor sintético queda en legacy/http-starter y no participa en la ejecución.
