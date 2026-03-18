"""Tool: batch_process"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_batch_process(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="batch_process",
                description="Batch Process - Part of Invoice & Receipt OCR",
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
        if name == "batch_process":
            # TODO: Implement batch_process
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "batch_process"}  ))]
