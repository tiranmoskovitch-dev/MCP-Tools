"""Tool: model_report"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_model_report(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="model_report",
                description="Model Report - Part of ML Model Monitor",
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
        if name == "model_report":
            # TODO: Implement model_report
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "model_report"}  ))]
