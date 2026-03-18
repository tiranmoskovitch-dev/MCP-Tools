"""Tool: compare_features"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_compare_features(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="compare_features",
                description="Compare Features - Part of Competitive Intelligence",
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
        if name == "compare_features":
            # TODO: Implement compare_features
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "compare_features"}  ))]
