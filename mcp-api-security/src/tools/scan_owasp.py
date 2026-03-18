"""Tool: scan_owasp"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_scan_owasp(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="scan_owasp",
                description="Scan Owasp - Part of API Security Scanner",
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
        if name == "scan_owasp":
            # TODO: Implement scan_owasp
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "scan_owasp"}  ))]
