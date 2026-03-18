"""Tool: categorize_expense"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_categorize_expense(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="categorize_expense",
                description="Categorize Expense - Part of Invoice & Receipt OCR",
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
        if name == "categorize_expense":
            # TODO: Implement categorize_expense
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "categorize_expense"}  ))]
