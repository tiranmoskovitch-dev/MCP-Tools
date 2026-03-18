"""Tool: export_opml"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_export_opml(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="export_opml",
                description="Export Opml - Part of RSS & Feed Aggregator",
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
        if name == "export_opml":
            # TODO: Implement export_opml
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "export_opml"}  ))]
