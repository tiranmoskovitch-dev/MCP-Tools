"""Tool: keyword_density"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_keyword_density(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="keyword_density",
                description="Keyword Density - Part of Text Analytics",
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
        if name == "keyword_density":
            # TODO: Implement keyword_density
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "keyword_density"}  ))]
