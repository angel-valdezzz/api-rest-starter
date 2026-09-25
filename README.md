# API REST Starter

Plantilla didáctica de pruebas de API REST con Python, Poetry, `requests`, `pytest` y reporte HTML. La documentación usa MkDocs Material y una paleta inspirada en EviDoc.

## Inicio rápido

Necesitas Python 3.11+ y Poetry.

```bash
poetry install
poetry run python -m pytest -v --html=reports/reporte.html --self-contained-html
poetry run mkdocs serve
```

Las cinco pruebas se conectan a una API local que pytest levanta y detiene automáticamente. No necesitas Internet ni variables de entorno para **ejecutar** las pruebas (sí necesitas acceso a los paquetes durante la instalación).

Abre `reports/reporte.html` para ver el resultado. El manual se abre en la dirección que muestra `mkdocs serve`; empieza en **Instalación y primera ejecución**. Para comprobar enlaces y generar la web estática usa `poetry run mkdocs build --strict`.

Consulta [`docs/plan.md`](docs/plan.md) para el plan de implementación y las siguientes mejoras.
