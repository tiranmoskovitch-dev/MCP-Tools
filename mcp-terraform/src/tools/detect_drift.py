"""Tool: detect_drift"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_detect_drift(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="detect_drift",
                description="Detect Drift - Part of Terraform Manager",
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
        if name == "detect_drift":
            # TODO: Implement detect_drift
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "detect_drift"}  ))]
