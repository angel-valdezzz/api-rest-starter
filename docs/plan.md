# Plan de implementación

## Primera versión: lista para usar

| Paso | Entregable | Comprobación |
| --- | --- | --- |
| 1 | Poetry con dependencias de pruebas y documentación | `poetry install` |
| 2 | Cinco casos GET y POST sobre una API local | `poetry run python -m pytest -v` |
| 3 | HTML con petición, respuesta, duración y resultado | Abrir `reports/reporte.html` |
| 4 | Manual introductorio y guía de adaptación | `poetry run mkdocs build --strict` |

## Al conectar una API real

1. Elige un recurso simple y revisa su contrato.
2. Adapta un GET exitoso y otro con error esperado.
3. Agrega POST solo si tienes datos de prueba y limpieza definidos.
4. Revisa que el reporte no revele datos sensibles.
5. Decide si hay repetición real que amerite fixtures o funciones auxiliares.

## Mejoras posibles, por prioridad

| Mejora | Cuándo vale la pena |
| --- | --- |
| Parametrización con `@pytest.mark.parametrize` | Varias entradas comparten exactamente la misma validación. |
| Selección de entorno y credenciales | Necesitas QA, staging o autenticación sin editar el código. |
| Validación de esquema/OpenAPI | El contrato tiene muchos campos y quieres comprobarlos automáticamente. |
| JUnit XML para CI | Ya existe un pipeline que consume resultados de prueba. |
| Allure o reporter propio | El equipo necesita navegación, adjuntos o trazabilidad que el HTML actual no cubre. |

**Criterio de diseño:** la primera versión solo requiere Python, Poetry, `requests`, `pytest`, `pytest-html` y MkDocs Material. Mantén el reporte de ejecución separado del manual de aprendizaje.
