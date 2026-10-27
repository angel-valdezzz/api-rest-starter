# Arquitectura API

Referencia: robotframework-api-testing. Se mantiene su división entre escenario, servicio,
assertions, configuración y datos. No se añaden capas de negocio vacías ni se emula una API.

| Responsabilidad | Implementación |
| --- | --- |
| Escenario | tests/test_user_lifecycle.py, tests/test_user_validation.py |
| HTTP | resources/services/users.py |
| Verificación | resources/assertions/users.py |
| Composición | resources/config/fixtures.py |
| Entorno | resources/config/settings.py |
| Ciclo de la API real opcional | resources/config/application.py |
| Preparación de filas y plantillas | resources/config/test_data.py |
| Entradas externas | data/tables, data/test, data/payloads |

La suite importa el plugin de composición en tests/conftest.py.
Las fixtures abren una requests.Session por caso y componen UsersService con sus settings.
Cada operación retorna la response real; los checks de negocio se ejecutan por separado y una vez.
Crear usuario registra su ID antes de que una assertion pueda fallar. El teardown intenta eliminar
todos los IDs propios y siempre cierra la sesión. No borra usuarios iniciales ni datos ajenos.

## Ejemplo de recorrido

1. Configuración carga una fila support o sales y copia la plantilla JSON.
2. El escenario pide crear un usuario al servicio.
3. user_created valida 201, UUID, campos y Location, y devuelve la identidad.
4. El escenario compone consulta, desactivación, reemplazo, borrado y confirmación de ausencia.
5. Las assertions comprueban los resultados; el teardown asegura la limpieza pendiente.

La API local se instala desde demo-users-api, fijada por commit en Poetry. Se ejecuta en un proceso
separado, desde un directorio temporal para evitar sombras de imports. CI y desarrollo usan
poetry run pytest --local-api; no hay un ejecutor genérico que envuelva Java o Node.

## Restricciones ejecutables

Los escenarios no importan clientes HTTP ni servicios de infraestructura y no contienen asserts crudos.
Los servicios no importan assertions ni cargadores de datos. Las assertions no crean sesiones ni envían HTTP.
tests/test_architecture.py verifica estas reglas también frente a imports con alias.
