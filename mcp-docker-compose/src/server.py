"""MCP Server: Docker Compose Architect
Generate, validate, optimize docker-compose configurations
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.generate_compose import register_generate_compose
from src.tools.validate_compose import register_validate_compose
from src.tools.optimize_resources import register_optimize_resources
from src.tools.add_service import register_add_service
from src.tools.health_check import register_health_check
from src.tools.network_diagram import register_network_diagram

server = Server("mcp-docker-compose")


def register_all_tools():
    register_generate_compose(server)
    register_validate_compose(server)
    register_optimize_resources(server)
    register_add_service(server)
    register_health_check(server)
    register_network_diagram(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
