# HTTP y REST desde cero

Una API permite que un programa solicite información o acciones a otro. En una prueba, tu código es el **cliente** y el servicio es el **servidor**.

## Una petición tiene piezas concretas

```text
POST http://127.0.0.1:puerto/users
Content-Type: application/json

{"name": "Angel"}
```

| Pieza | Para qué sirve | Ejemplo |
| --- | --- | --- |
| Método | La acción solicitada | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| URL/ruta | El recurso al que llamas | `/users/1` |
| Parámetros de consulta | Opciones en la URL | `?page=2` |
| Encabezados | Metadatos, tipo de contenido, autenticación | `Content-Type: application/json` |
| Cuerpo | Datos enviados cuando corresponda | `{"name": "Angel"}` |

La **respuesta** trae un código de estado, encabezados y a veces un cuerpo:

```json
{"id": 2, "name": "Angel"}
```

## Qué significan los estados

| Código | Interpretación habitual | Qué conviene verificar |
| --- | --- | --- |
| `200` | La consulta o acción se completó | Datos y estructura esperados |
| `201` | Se creó un recurso | Identificador y datos creados |
| `204` | Éxito sin contenido | Código; no intentes leer JSON |
| `400` | Solicitud inválida | Mensaje de error, validación |
| `401` | Falta autenticación válida | Restricción de acceso |
| `403` | Acceso denegado | Permisos |
| `404` | Recurso no encontrado | Mensaje o contrato de error |
| `500` | Error del servidor | Investigar el fallo |

Los códigos comunican una categoría de resultado; el contrato concreto de tu API define qué respuestas son correctas para cada caso. Por eso una prueba de `404` puede **pasar**.

## Tu primer diseño de casos

Para `POST /users`, escribe primero el comportamiento esperado:

| Caso | Entrada | Estado esperado | Dato que revisarás |
| --- | --- | --- | --- |
| Crear usuario | Nombre válido | `201` | El nombre devuelto |
| Rechazar datos vacíos | `{}` | `400` | Mensaje de validación |

Una aserción comprueba el resultado observado contra ese esperado. Sigue con [Peticiones con requests](requests.md).
