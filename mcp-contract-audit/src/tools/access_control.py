"""Tool: access_control"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_access_control(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="access_control",
                description="Access Control - Part of Smart Contract Auditor",
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
        if name == "access_control":
            # TODO: Implement access_control
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "access_control"}  ))]
