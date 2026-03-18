"""Tool: import_opml"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_import_opml(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="import_opml",
                description="Import Opml - Part of RSS & Feed Aggregator",
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
        if name == "import_opml":
            # TODO: Implement import_opml
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "import_opml"}  ))]
