"""Tool: dns_lookup"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_dns_lookup(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="dns_lookup",
                description="Dns Lookup - Part of Network Diagnostics",
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
        if name == "dns_lookup":
            # TODO: Implement dns_lookup
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "dns_lookup"}  ))]
