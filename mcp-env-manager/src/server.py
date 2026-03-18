"""MCP Server: Environment Manager
Sync .env files across environments, secret rotation, validation
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.sync_envs import register_sync_envs
from src.tools.diff_envs import register_diff_envs
from src.tools.validate_env import register_validate_env
from src.tools.rotate_secret import register_rotate_secret
from src.tools.encrypt_env import register_encrypt_env
from src.tools.generate_template import register_generate_template

server = Server("mcp-env-manager")


def register_all_tools():
    register_sync_envs(server)
    register_diff_envs(server)
    register_validate_env(server)
    register_rotate_secret(server)
    register_encrypt_env(server)
    register_generate_template(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
