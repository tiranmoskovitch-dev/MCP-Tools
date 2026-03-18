"""Tool: fake_company"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_fake_company(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="fake_company",
                description="Fake Company - Part of Lorem & Data Generator",
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
        if name == "fake_company":
            # TODO: Implement fake_company
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "fake_company"}  ))]
