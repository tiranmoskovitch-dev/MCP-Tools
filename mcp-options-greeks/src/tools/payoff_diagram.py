"""Tool: payoff_diagram"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_payoff_diagram(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="payoff_diagram",
                description="Payoff Diagram - Part of Options Greeks Calculator",
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
        if name == "payoff_diagram":
            # TODO: Implement payoff_diagram
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "payoff_diagram"}  ))]
