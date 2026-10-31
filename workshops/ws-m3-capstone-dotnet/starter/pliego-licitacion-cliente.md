# Pliego de Negocio del Cliente: GuardiaCloud Command Center v2.0

**De:** Dirección de Operaciones Regionales & Riesgo Operativo (Banca y Seguros)
**Para:** Equipo de Ingeniería `.NET` de la Consultora
**Asunto:** Requerimientos urgentes para el lanzamiento de Command Center v2.0

Hola equipo:

Necesitamos cerrar cuatro entregas críticas sobre `GuardiaCloud.CommandCenter.Api` antes de la auditoría del comité bancario:

1. **[Urgente — BUG-301] Duplicación de penalidades cuando el bus de eventos reintenta webhooks:**
   Nuestro colector de monitoreo reintenta el envío de webhooks (`POST /api/command-center/webhooks/incident-event`) cuando hay microcortes de red. Hoy vimos que si llega dos veces el mismo evento de transición, el sistema suma minutos de penalidad duplicados o pisa el estado. Necesitamos que sea **idempotente**.

2. **[FEAT-301] Motor de Escalamiento Proactivo antes de que venza el SLA:**
   No nos sirve enterarnos recién cuando el SLA ya venció. Queremos un endpoint (`POST /api/command-center/escalations/evaluate`) que revise un incidente activo y dispare una alerta temprana cuando ya consumió buena parte de su presupuesto de tiempo, pero sin inundar de alertas repetidas al canal de guardia si alguien consulta dos veces seguidas.

3. **[FEAT-302] Excepciones por Fuerza Mayor (Caída de Proveedor Externo / BCRA / Nube):**
   Cuando el incidente se debe a una caída masiva externa (ej. red interbancaria Coelsa o caída regional de nube), necesitamos poder registrar una **Excepción de Fuerza Mayor** (`POST /api/command-center/exemptions`) para que ese incidente quede exento de penalidad económica en la liquidación mensual. Por auditoría interna, no puede aprobarlo una sola persona ni con cualquier texto libre.

4. **[FEAT-303] Tablero Ejecutivo Consolidado por Tier de Cliente:**
   Necesitamos el endpoint de cabecera (`GET /api/command-center/dashboard/{clientTier}`) y su vista de tablero para que el Director de Cuenta vea en tiempo real cuántos incidentes tiene el tier, cuántos están vencidos, cuántos están en alerta temprana, cuántos tienen exención de fuerza mayor y cuál es la exposición económica acumulada en USD.

> **Nota para la Unidad 3.1:** Este pliego tiene definiciones de negocio deliberadamente abiertas (umbrales exactos, ventana de enfriamiento de alertas, formato de doble firma de exención, códigos de error RFC 9457, etc.). Usen su agente para auditar qué falta preguntar y preparen el cuestionario para las dos rondas de entrevista con el cliente (instructor).
