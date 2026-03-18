"""MCP Server: Kubernetes Cluster Manager
Pod health, resource optimization, log aggregation, scaling
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.cluster_health import register_cluster_health
from src.tools.pod_status import register_pod_status
from src.tools.resource_optimize import register_resource_optimize
from src.tools.aggregate_logs import register_aggregate_logs
from src.tools.scaling_rules import register_scaling_rules
from src.tools.node_analysis import register_node_analysis

server = Server("mcp-k8s-manager")


def register_all_tools():
    register_cluster_health(server)
    register_pod_status(server)
    register_resource_optimize(server)
    register_aggregate_logs(server)
    register_scaling_rules(server)
    register_node_analysis(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
