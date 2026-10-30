# Pedido de negocio (Mensaje de Slack del Gerente de Operaciones)

**De:** Martín (Gerente de Operaciones y Guardia 24x7)
**Para:** Equipo de Ingeniería (.NET)
**Asunto:** Urgente: pausar el reloj de SLA cuando esperamos al cliente + reporte de incidente mal marcado como vencido

---

> Hola equipo, ¿cómo andan?
>
> Necesitamos meter un cambio urgente en la API de SLA (`GuardiaCloud.Sla.Api`) porque este mes los bancos nos objetaron tres multas.
>
> **1) Hoy el reloj de SLA corre sin parar desde que se abre el incidente (`OpenedAtUtc`)**, incluso cuando nosotros ya le pedimos logs o acceso VPN al cliente y el cliente tarda 3 horas en contestarnos. Necesitamos poder **pausar el SLA** cuando estamos esperando al cliente (`WaitingForCustomer` o algo así) y **volver a prenderlo** cuando el cliente nos responde. Obviamente ese tiempo en pausa no tiene que contar como tiempo activo consumido y tiene que correr para adelante el vencimiento (`EffectiveDeadlineUtc`), guardando el historial de por qué se pausó y quién lo pausó para la auditoría del banco.
>
> **2) Además, ayer cerramos un incidente P1 a los 40 minutos (adentro de los 60 min del SLA)**, pero hoy a la mañana cuando el dashboard consultó `GET /api/incidents/{id}/sla` ¡aparece como `isBreached: true` con más de 1000 minutos consumidos! Fíjense qué pasa ahí porque nos está ensuciando todo el tablero mensual.
>
> ¿Lo pueden tener listo hoy? Es un par de endpoints nomás. ¡Gracias!
