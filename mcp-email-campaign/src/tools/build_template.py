"""Tool: build_template"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_build_template(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="build_template",
                description="Build Template - Part of Email Campaign Builder",
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
        if name == "build_template":
            # TODO: Implement build_template
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "build_template"}  ))]
