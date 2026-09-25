# Instalación y primera ejecución

Al terminar tendrás cinco pruebas aprobadas y un archivo `reports/reporte.html`.

## 1. Prepara Python y Poetry

Instala Python 3.11 o posterior y Poetry. Verifica que ambos funcionen:

```bash
python --version
poetry --version
```

Si `python` no se reconoce en Windows, prueba `py --version`. Instala Poetry siguiendo su [guía oficial](https://python-poetry.org/docs/#installation).

## 2. Instala el proyecto

Abre una terminal en la carpeta que contiene `pyproject.toml` y ejecuta:

```bash
poetry install
```

Poetry instala `requests`, `pytest`, `pytest-html` y MkDocs Material. El proyecto es una plantilla de pruebas, no un paquete para publicar.

## 3. Ejecuta las pruebas

```bash
poetry run python -m pytest -v --html=reports/reporte.html --self-contained-html
```

Abre `reports/reporte.html` en el navegador. Encontrarás cinco resultados y, en el detalle de cada caso, la petición y la respuesta. Si vuelves a ejecutar, se actualiza el mismo archivo.

!!! info "No tienes que iniciar ningún servidor"
    La fixture `api_url` de `tests/conftest.py` inicia temporalmente la API local en un puerto libre. Al acabar las pruebas la apaga. No se requiere Internet durante la ejecución.

## 4. Lee el manual en el navegador

```bash
poetry run mkdocs serve
```

Abre la dirección que muestre la terminal (habitualmente `http://127.0.0.1:8000`). Para salir, pulsa `Ctrl+C`. Para generar el sitio estático:

```bash
poetry run mkdocs build --strict
```

!!! warning "¿Hay errores al instalar?"
    Revisa que la terminal esté dentro del proyecto y que Poetry esté instalado. Si el error ocurre descargando paquetes, necesitas acceso al repositorio de paquetes durante `poetry install`; después las pruebas de ejemplo funcionan sin Internet.
