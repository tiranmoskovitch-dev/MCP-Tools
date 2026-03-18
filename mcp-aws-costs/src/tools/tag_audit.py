"""Tool: tag_audit"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_tag_audit(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="tag_audit",
                description="Tag Audit - Part of AWS Cost Optimizer",
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
        if name == "tag_audit":
            # TODO: Implement tag_audit
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "tag_audit"}  ))]
