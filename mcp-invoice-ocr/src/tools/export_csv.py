"""Tool: export_csv"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_export_csv(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="export_csv",
                description="Export Csv - Part of Invoice & Receipt OCR",
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
        if name == "export_csv":
            # TODO: Implement export_csv
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "export_csv"}  ))]
