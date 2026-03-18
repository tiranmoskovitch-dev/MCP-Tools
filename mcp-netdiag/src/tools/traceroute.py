"""Tool: traceroute"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_traceroute(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="traceroute",
                description="Traceroute - Part of Network Diagnostics",
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
        if name == "traceroute":
            # TODO: Implement traceroute
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "traceroute"}  ))]
