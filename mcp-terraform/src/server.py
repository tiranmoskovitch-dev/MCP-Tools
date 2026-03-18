"""MCP Server: Terraform Manager
Plan/apply, state inspection, drift detection, module generator
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.plan_changes import register_plan_changes
from src.tools.inspect_state import register_inspect_state
from src.tools.detect_drift import register_detect_drift
from src.tools.generate_module import register_generate_module
from src.tools.validate_config import register_validate_config
from src.tools.cost_estimate import register_cost_estimate

server = Server("mcp-terraform")


def register_all_tools():
    register_plan_changes(server)
    register_inspect_state(server)
    register_detect_drift(server)
    register_generate_module(server)
    register_validate_config(server)
    register_cost_estimate(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
