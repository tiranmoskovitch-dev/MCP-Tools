"""Tool: tech_debt_score"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_tech_debt_score(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="tech_debt_score",
                description="Tech Debt Score - Part of Git Repository Analyzer",
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
        if name == "tech_debt_score":
            # TODO: Implement tech_debt_score
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "tech_debt_score"}  ))]
