"""Tool: generate_migration"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_generate_migration(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="generate_migration",
                description="Generate Migration - Part of Database Schema Differ",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "input": {"type": "string", "description": "Input parameter"}
                    },
                    "required": ["input"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "generate_migration":
            # TODO: Implement generate_migration
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "generate_migration"}  ))]
