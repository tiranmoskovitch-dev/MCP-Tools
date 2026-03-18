"""Tool: extract_receipt"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_extract_receipt(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="extract_receipt",
                description="Extract Receipt - Part of Invoice & Receipt OCR",
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
        if name == "extract_receipt":
            # TODO: Implement extract_receipt
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "extract_receipt"}  ))]
