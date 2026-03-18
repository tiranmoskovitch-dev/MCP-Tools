"""Tool: reentrancy_check"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_reentrancy_check(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="reentrancy_check",
                description="Reentrancy Check - Part of Smart Contract Auditor",
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
        if name == "reentrancy_check":
            # TODO: Implement reentrancy_check
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "reentrancy_check"}  ))]
