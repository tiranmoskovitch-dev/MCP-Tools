"""Tool: jwt_decode"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_jwt_decode(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="jwt_decode",
                description="Jwt Decode - Part of Hash & Crypto Utilities",
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
        if name == "jwt_decode":
            # TODO: Implement jwt_decode
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "jwt_decode"}  ))]
