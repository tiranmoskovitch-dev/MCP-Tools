"""MCP Server: Database Schema Differ
Compare schemas, generate migrations, detect drift across databases
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.compare_schemas import register_compare_schemas
from src.tools.generate_migration import register_generate_migration
from src.tools.detect_drift import register_detect_drift
from src.tools.visualize_schema import register_visualize_schema
from src.tools.export_erd import register_export_erd
from src.tools.validate_migration import register_validate_migration

server = Server("mcp-schema-diff")


def register_all_tools():
    register_compare_schemas(server)
    register_generate_migration(server)
    register_detect_drift(server)
    register_visualize_schema(server)
    register_export_erd(server)
    register_validate_migration(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
