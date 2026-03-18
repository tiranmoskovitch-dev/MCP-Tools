"""Tool: compare_schemas"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_compare_schemas(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="compare_schemas",
                description="Compare Schemas - Part of Database Schema Differ",
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
        if name == "compare_schemas":
            # TODO: Implement compare_schemas
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "compare_schemas"}  ))]
