# Reglas de Ingeniería .NET 10 — GuardiaCloud.Sla

## Comandos de Verificación Obligatorios
- Compilar sin warnings: `dotnet build GuardiaCloud.Sla.sln --no-restore /p:TreatWarningsAsErrors=true`
- Ejecutar suite de pruebas: `dotnet test GuardiaCloud.Sla.sln --no-build`

## Invariantes de Arquitectura y Código C# 13
1. **Target Framework:** `net10.0`, `Nullable=enable`, `TreatWarningsAsErrors=true`.
2. **Tiempo Determinista:** Prohibido usar `DateTime.Now` o `DateTime.UtcNow` directamente en servicios de negocio; inyectá siempre `System.TimeProvider`.
3. **Contratos HTTP:** Todo endpoint ASP.NET Core Minimal API recibe `CancellationToken` y devuelve errores 4xx/5xx en formato `ProblemDetails` (RFC 9457) con `extensions["errorCode"]`.
4. **Seguridad y Performance:** Prohibido hardcodear secretos en código/configuración o ejecutar consultas `N+1` dentro de bucles `foreach`.
5. **Tokens de UI:** Todo componente visual debe respetar los colores semánticos de `ui/design-tokens.json` y las propiedades exactas de `IncidentSlaCardDto`.
