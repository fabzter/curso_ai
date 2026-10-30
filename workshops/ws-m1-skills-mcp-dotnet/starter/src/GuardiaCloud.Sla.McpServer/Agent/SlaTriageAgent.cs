using System.Runtime.CompilerServices;
using GuardiaCloud.Sla.McpServer.McpTools;
using Microsoft.Extensions.AI;

namespace GuardiaCloud.Sla.McpServer.Agent;

public sealed record SlaTriageReport(
    string IncidentId,
    string FinalSummary,
    IReadOnlyList<string> InvokedToolNames,
    int TotalMessagesCount);

public sealed class SlaTriageAgent(SlaMcpTools tools, IChatClient innerChatClient)
{
    private readonly SlaMcpTools _tools = tools;
    private readonly IChatClient _innerChatClient = innerChatClient;

    public IReadOnlyList<AITool> CreateRegisteredTools()
    {
        // En el starter solo se registra get_client_sla_policy.
        // TODO (Fase 3 - Unidad 1.3B): Agregar inspect_incident_sla_status y validate_rfc9457_contract con AIFunctionFactory.Create(...).
        return
        [
            AIFunctionFactory.Create(_tools.GetClientSlaPolicy, "get_client_sla_policy")
        ];
    }

    public Task<SlaTriageReport> RunTriageAsync(string incidentId, CancellationToken cancellationToken = default)
    {
        _ = _innerChatClient;
        _ = incidentId;
        _ = cancellationToken;
        throw new NotImplementedException(
            "TODO (Fase 3 - Unidad 1.3B): Construir el pipeline IChatClient con .AsBuilder().UseFunctionInvocation(...) y límites de parada.");
    }
}

/// <summary>
/// Cliente IChatClient determinista provisto para el aula y tests xUnit (simula el bucle de tool-calling sin requerir API key externa).
/// </summary>
public sealed class DeterministicTriageChatClient(string targetIncidentId = "INC-2026-1002") : IChatClient
{
    private readonly string _targetIncidentId = targetIncidentId;

    public Task<ChatResponse> GetResponseAsync(
        IEnumerable<ChatMessage> messages,
        ChatOptions? options = null,
        CancellationToken cancellationToken = default)
    {
        var history = messages.ToList();
        var functionResults = history.SelectMany(m => m.Contents.OfType<FunctionResultContent>()).ToList();

        if (functionResults.Count == 0)
        {
            var callInspect = new FunctionCallContent(
                callId: "call-inspect-1",
                name: "inspect_incident_sla_status",
                arguments: new Dictionary<string, object?> { ["incidentId"] = _targetIncidentId });

            return Task.FromResult(new ChatResponse(new ChatMessage(ChatRole.Assistant, [callInspect])));
        }

        if (functionResults.Count == 1)
        {
            var callPolicy = new FunctionCallContent(
                callId: "call-policy-2",
                name: "get_client_sla_policy",
                arguments: new Dictionary<string, object?>
                {
                    ["clientTier"] = "Bancario-Tier1",
                    ["severity"] = "P1"
                });

            return Task.FromResult(new ChatResponse(new ChatMessage(ChatRole.Assistant, [callPolicy])));
        }

        var auditPayload = functionResults[0].Result?.ToString() ?? string.Empty;
        var policyPayload = functionResults[1].Result?.ToString() ?? string.Empty;

        var synthesis =
            $"Dictamen de Triage para {_targetIncidentId}: Estado auditado vía MCP tools. " +
            $"Resultado auditoría: {auditPayload} | Política aplicada: {policyPayload}";

        return Task.FromResult(new ChatResponse(new ChatMessage(ChatRole.Assistant, synthesis)));
    }

    public async IAsyncEnumerable<ChatResponseUpdate> GetStreamingResponseAsync(
        IEnumerable<ChatMessage> messages,
        ChatOptions? options = null,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        var response = await GetResponseAsync(messages, options, cancellationToken);
        yield return new ChatResponseUpdate(ChatRole.Assistant, response.Text);
    }

    public object? GetService(Type serviceType, object? serviceKey = null) =>
        serviceKey is null && serviceType.IsInstanceOfType(this) ? this : null;

    public void Dispose()
    {
    }
}
