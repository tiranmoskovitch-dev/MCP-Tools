"""Tool: replay_request"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_replay_request(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="replay_request",
                description="Replay Request - Part of Webhook Tester & Logger",
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
        if name == "replay_request":
            # TODO: Implement replay_request
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "replay_request"}  ))]
