"""Tool: security_score"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_security_score(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="security_score",
                description="Security Score - Part of Cloud Security Auditor",
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
        if name == "security_score":
            # TODO: Implement security_score
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "security_score"}  ))]
