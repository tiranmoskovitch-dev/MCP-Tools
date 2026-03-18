"""Tool: readability_score"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_readability_score(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="readability_score",
                description="Readability Score - Part of Text Analytics",
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
        if name == "readability_score":
            # TODO: Implement readability_score
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "readability_score"}  ))]
