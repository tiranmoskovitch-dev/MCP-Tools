"""Tool: fake_credit_card"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_fake_credit_card(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="fake_credit_card",
                description="Fake Credit Card - Part of Lorem & Data Generator",
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
        if name == "fake_credit_card":
            # TODO: Implement fake_credit_card
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "fake_credit_card"}  ))]
