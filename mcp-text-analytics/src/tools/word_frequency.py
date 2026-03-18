"""Tool: word_frequency"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_word_frequency(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="word_frequency",
                description="Word Frequency - Part of Text Analytics",
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
        if name == "word_frequency":
            # TODO: Implement word_frequency
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "word_frequency"}  ))]
