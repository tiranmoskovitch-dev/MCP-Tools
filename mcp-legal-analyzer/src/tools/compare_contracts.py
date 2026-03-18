"""Tool: compare_contracts"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_compare_contracts(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="compare_contracts",
                description="Compare Contracts - Part of Legal Document Analyzer",
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
        if name == "compare_contracts":
            # TODO: Implement compare_contracts
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "compare_contracts"}  ))]
