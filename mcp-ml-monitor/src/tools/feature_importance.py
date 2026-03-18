"""Tool: feature_importance"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_feature_importance(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="feature_importance",
                description="Feature Importance - Part of ML Model Monitor",
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
        if name == "feature_importance":
            # TODO: Implement feature_importance
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "feature_importance"}  ))]
