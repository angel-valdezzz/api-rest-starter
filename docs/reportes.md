# Leer el reporte HTML

Genera un archivo independiente:

```bash
poetry run python -m pytest -v --html=reports/reporte.html --self-contained-html
```

En `reports/reporte.html` encontrarás el total de pruebas, su resultado y duración. Abre un caso para ver el detalle. Esta plantilla añade un bloque **Petición y respuesta** con:

| Campo | Qué te ayuda a responder |
| --- | --- |
| Método y URL | ¿A qué endpoint se llamó? |
| Cuerpo enviado | ¿Qué datos salieron del test? |
| Estado recibido | ¿Qué contestó HTTP? |
| Tiempo HTTP | ¿Cuánto tardó esa llamada? |
| Respuesta | ¿Qué devolvió el servicio? |

El tiempo HTTP mostrado en el bloque corresponde a la petición. La duración del caso que muestra pytest incluye además Python y las aserciones.

**Límites deliberados:** se muestran hasta 1000 caracteres del cuerpo enviado y 2000 de la respuesta. No hay historial, gráficas de tendencias ni un panel personalizado. El HTML deja ver lo necesario para revisar una primera ejecución.

El archivo generado queda en `reports/`, fuera de `docs/`: el manual explica cómo usar la plantilla; el reporte registra una ejecución concreta.

!!! warning "Antes de compartir reportes reales"
    Retira o enmascara identificadores personales y secretos en `registrar_http()`. Los reportes de ejemplo no contienen información real.
