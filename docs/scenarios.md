# Escenarios de negocio

- CRUD completo con filas support y sales: creación, consulta, PATCH, PUT, DELETE y ausencia.
- Correo duplicado: conflicto esperado, conservando al usuario original.
- Activación/desactivación, conflictos de estado y filtro de usuarios inactivos.
- Estadísticas antes y después de crear un usuario.
- Filtros combinados y paginación.
- Entradas inválidas desde data/test: nombre/email, rol y campos desconocidos.
- Paginación inválida: limit 0, offset negativo y limit mayor que el máximo.
- PATCH con null rechazado y usuario original sin modificación.
- Health público y credenciales ausentes/incorrectas.
- Usuario inexistente identificado por UUID válido.

Las plantillas son JSON válido. La preparación conserva tipos y trabaja sobre copias.
Los datos y expectativas pertenecen a las entradas o assertions; los tests no implementan HTTP.
