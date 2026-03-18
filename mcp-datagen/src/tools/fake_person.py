"""Tool: fake_person"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_fake_person(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="fake_person",
                description="Fake Person - Part of Lorem & Data Generator",
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
        if name == "fake_person":
            # TODO: Implement fake_person
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "fake_person"}  ))]
