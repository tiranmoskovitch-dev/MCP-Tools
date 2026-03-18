"""Tool: diff_envs"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_diff_envs(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="diff_envs",
                description="Diff Envs - Part of Environment Manager",
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
        if name == "diff_envs":
            # TODO: Implement diff_envs
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "diff_envs"}  ))]
