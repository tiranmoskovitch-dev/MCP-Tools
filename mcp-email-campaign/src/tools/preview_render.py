"""Tool: preview_render"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_preview_render(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="preview_render",
                description="Preview Render - Part of Email Campaign Builder",
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
        if name == "preview_render":
            # TODO: Implement preview_render
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "preview_render"}  ))]
