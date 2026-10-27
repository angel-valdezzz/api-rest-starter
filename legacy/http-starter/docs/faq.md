# Problemas frecuentes

??? question "`poetry` no se reconoce"
    Instala Poetry desde su guía oficial y abre una terminal nueva. Verifica con `poetry --version`.

??? question "`python` no se reconoce en Windows"
    Ejecuta `py --version`. Para pytest puedes usar `poetry run python -m pytest`; Poetry resuelve el intérprete de su entorno.

??? question "Veo `ModuleNotFoundError: demo_api`"
    Ejecuta desde la carpeta raíz, donde está `pyproject.toml`, con `poetry run python -m pytest`. No lances `tests/test_api.py` como un script suelto.

??? question "Una prueba da 404, ¿por qué aparece aprobada?"
    Una de las pruebas comprueba que un usuario inexistente responda precisamente `404`. Revisa el `assert` de ese caso.

??? question "El HTML no aparece"
    Incluye `--html=reports/reporte.html` en el comando. La carpeta se crea al generar el reporte.

??? question "MkDocs muestra una página antigua"
    Mientras editas usa `poetry run mkdocs serve` y recarga el navegador. Para compartir archivos estáticos vuelve a ejecutar `poetry run mkdocs build --strict`.

??? question "Quiero probar mi propio servicio"
    Sigue [Adaptar las pruebas](adaptar.md). Las rutas y datos del ejemplo local no describen tu API.
