"""Tool: analyst_ratings"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_analyst_ratings(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="analyst_ratings",
                description="Analyst Ratings - Part of Stock Sentiment Analyzer",
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
        if name == "analyst_ratings":
            # TODO: Implement analyst_ratings
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "analyst_ratings"}  ))]
