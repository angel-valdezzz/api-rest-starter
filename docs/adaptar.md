# Adaptar las pruebas a tu API

Empieza con **una llamada** de tu servicio. Abre `tests/test_api.py`, copia una prueba y sustituye la URL, datos y aserciones.

```python
def test_consultar_producto(extras):
    response = requests.get("https://mi-api.example/products/1", timeout=10)
    registrar_http(extras, response)

    assert response.status_code == 200
    assert response.json()["id"] == 1
```

Esta prueba no necesita `api_url`: la fixture solo existe para la demostración local. Cuando ya uses exclusivamente tu servicio, puedes retirar `demo_api.py` y `tests/conftest.py`.

## Orden recomendado

1. Identifica método, ruta, headers y cuerpo en la documentación de tu API o en Postman.
2. Escribe un caso feliz con una aserción sobre el estado y otra sobre un dato relevante.
3. Añade un caso de error esperado: datos inválidos, inexistente o falta de permisos.
4. Ejecuta ambos y abre el HTML.
5. Solo si repites código varias veces, extrae una función o fixture.

Para un token temporal en una prueba real podrías pasar `headers={"Authorization": "Bearer ..."}`, pero no guardes el valor real en el repositorio ni lo adjuntes al reporte. Si más adelante necesitas secretos, incorporaremos una forma segura de configurarlos.

!!! info "Datos de prueba"
    Para `POST`, usa datos controlados y verifica si el servicio crea registros persistentes. Si los crea, planifica su limpieza antes de ejecutar repetidamente contra un entorno compartido.
