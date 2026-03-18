"""Tool: dependency_tree"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_dependency_tree(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="dependency_tree",
                description="Dependency Tree - Part of Dependency Auditor",
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
        if name == "dependency_tree":
            # TODO: Implement dependency_tree
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "dependency_tree"}  ))]
