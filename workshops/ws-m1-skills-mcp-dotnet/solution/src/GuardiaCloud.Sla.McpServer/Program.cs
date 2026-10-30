using GuardiaCloud.Sla.McpServer.Infrastructure;
using GuardiaCloud.Sla.McpServer.McpTools;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace GuardiaCloud.Sla.McpServer;

public static class Program
{
    public static async Task Main(string[] args)
    {
        var builder = CreateHostBuilder(args);
        await builder.Build().RunAsync();
    }

    public static HostApplicationBuilder CreateHostBuilder(string[] args)
    {
        var builder = Host.CreateApplicationBuilder(args);

        // Regla crítica de MCP sobre stdio: enviar todos los logs a stderr para no contaminar stdout (JSON-RPC)
        builder.Logging.AddConsole(options =>
        {
            options.LogToStandardErrorThreshold = LogLevel.Trace;
        });

        builder.Services.AddSingleton(TimeProvider.System);
        builder.Services.AddSingleton<InMemorySlaCatalogStore>();
        builder.Services.AddSingleton<SlaMcpTools>();

        builder.Services
            .AddMcpServer()
            .WithStdioServerTransport()
            .WithTools<SlaMcpTools>();

        return builder;
    }
}
