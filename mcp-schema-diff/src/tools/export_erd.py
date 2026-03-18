"""Tool: export_erd"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_export_erd(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="export_erd",
                description="Export Erd - Part of Database Schema Differ",
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
        if name == "export_erd":
            # TODO: Implement export_erd
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "export_erd"}  ))]
