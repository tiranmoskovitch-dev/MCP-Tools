"""Tool: sec_filings"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_sec_filings(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="sec_filings",
                description="Sec Filings - Part of Stock Sentiment Analyzer",
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
        if name == "sec_filings":
            # TODO: Implement sec_filings
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "sec_filings"}  ))]
