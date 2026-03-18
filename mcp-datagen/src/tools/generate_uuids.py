"""Tool: generate_uuids"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_generate_uuids(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="generate_uuids",
                description="Generate Uuids - Part of Lorem & Data Generator",
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
        if name == "generate_uuids":
            # TODO: Implement generate_uuids
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "generate_uuids"}  ))]
