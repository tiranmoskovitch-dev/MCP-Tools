"""MCP Server: Webhook Tester & Logger
Receive, log, replay webhooks, mock API responses
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.create_endpoint import register_create_endpoint
from src.tools.list_requests import register_list_requests
from src.tools.replay_request import register_replay_request
from src.tools.mock_response import register_mock_response
from src.tools.webhook_stats import register_webhook_stats
from src.tools.export_logs import register_export_logs

server = Server("mcp-webhook")


def register_all_tools():
    register_create_endpoint(server)
    register_list_requests(server)
    register_replay_request(server)
    register_mock_response(server)
    register_webhook_stats(server)
    register_export_logs(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
