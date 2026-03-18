"""Tool: mortgage_calc"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_mortgage_calc(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="mortgage_calc",
                description="Mortgage Calc - Part of Real Estate Analyzer",
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
        if name == "mortgage_calc":
            # TODO: Implement mortgage_calc
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "mortgage_calc"}  ))]
