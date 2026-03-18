"""Tool: export_results"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_export_results(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="export_results",
                description="Export Results - Part of API Load Tester",
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
        if name == "export_results":
            # TODO: Implement export_results
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "export_results"}  ))]
