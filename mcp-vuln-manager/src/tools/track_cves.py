"""Tool: track_cves"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_track_cves(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="track_cves",
                description="Track Cves - Part of Vulnerability Manager",
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
        if name == "track_cves":
            # TODO: Implement track_cves
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "track_cves"}  ))]
