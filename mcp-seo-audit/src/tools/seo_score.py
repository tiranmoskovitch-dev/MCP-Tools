"""Tool: seo_score"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_seo_score(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="seo_score",
                description="Seo Score - Part of SEO Site Auditor",
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
        if name == "seo_score":
            # TODO: Implement seo_score
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "seo_score"}  ))]
