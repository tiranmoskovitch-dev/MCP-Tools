"""Tool: nda_review"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_nda_review(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="nda_review",
                description="Nda Review - Part of Legal Document Analyzer",
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
        if name == "nda_review":
            # TODO: Implement nda_review
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "nda_review"}  ))]
