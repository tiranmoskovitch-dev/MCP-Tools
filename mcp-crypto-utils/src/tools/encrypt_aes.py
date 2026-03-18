"""Tool: encrypt_aes"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_encrypt_aes(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="encrypt_aes",
                description="Encrypt Aes - Part of Hash & Crypto Utilities",
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
        if name == "encrypt_aes":
            # TODO: Implement encrypt_aes
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "encrypt_aes"}  ))]
