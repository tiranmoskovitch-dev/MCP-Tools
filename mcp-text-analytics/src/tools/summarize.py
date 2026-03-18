"""Tool: summarize"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_summarize(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="summarize",
                description="Summarize - Part of Text Analytics",
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
        if name == "summarize":
            # TODO: Implement summarize
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "summarize"}  ))]
