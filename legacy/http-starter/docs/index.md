<div class="api-hero">
  <span class="eyebrow">Manual de usuario · API REST</span>
  <h1>Prueba servicios con Python</h1>
  <p>Una ruta práctica desde tu primera petición HTTP hasta un reporte de pruebas que puedes compartir.</p>
  <a href="primeros-pasos/">Ejecutar la primera prueba →</a>
</div>

## Tu recorrido

<div class="api-cards">
  <div class="api-card"><strong>01 · Comprende</strong><span>Qué envía el cliente y qué responde la API.</span></div>
  <div class="api-card"><strong>02 · Ejecuta</strong><span>Corre cinco pruebas sin cuentas ni servidores externos.</span></div>
  <div class="api-card"><strong>03 · Adapta</strong><span>Cambia una URL y crea tus propios casos.</span></div>
  <div class="api-card"><strong>04 · Comparte</strong><span>Abre un reporte HTML con el resultado y el intercambio HTTP.</span></div>
</div>

!!! tip "Si nunca has probado una API"
    Sigue [HTTP y REST desde cero](tutorial/http.md), después [la primera ejecución](primeros-pasos.md) y finalmente [las pruebas con pytest](tutorial/pytest.md).

El ejemplo usa llamadas directas de `requests`, sin cliente propio ni variables de entorno. `pytest` inicia una API de demostración local y la apaga al terminar. [Consulta la estructura](plantilla.md) para ver qué hace cada archivo.
