"""Tool: evidence_collect"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_evidence_collect(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="evidence_collect",
                description="Evidence Collect - Part of Compliance Report Generator",
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
        if name == "evidence_collect":
            # TODO: Implement evidence_collect
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "evidence_collect"}  ))]
