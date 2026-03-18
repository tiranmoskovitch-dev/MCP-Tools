"""Tool: send_test"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_send_test(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="send_test",
                description="Send Test - Part of Email Campaign Builder",
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
        if name == "send_test":
            # TODO: Implement send_test
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "send_test"}  ))]
