using GuardiaCloud.Sla.Api.Infrastructure;

namespace GuardiaCloud.Sla.Api.Domain;

// ❌ VIOLACIÓN ARQUITECTÓNICA INTENCIONAL (Deuda técnica generada por IA sin Harness ni Oráculo):
// 1. No es 'sealed' ni 'static'.
// 2. Está en el namespace 'Domain' pero acopla directamente con 'Infrastructure.InMemoryIncidentStore'.
// 3. Usa DateTimeOffset.UtcNow en lugar de TimeProvider.
// En la Fase 2, al activar las reglas de NetArchTest en ArchitectureOracleTests.cs, este archivo hará fallar el oráculo
// y deberá ser eliminado o refactorizado.
public class LegacyVibeCodedHelper
{
    public string DumpQuickStatus(InMemoryIncidentStore store) =>
        $"Snapshot@{DateTimeOffset.UtcNow:O}: {store.GetAll().Count} incidents";
}
