"""Tool: summary_report"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_summary_report(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="summary_report",
                description="Summary Report - Part of Legal Document Analyzer",
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
        if name == "summary_report":
            # TODO: Implement summary_report
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "summary_report"}  ))]
