"""Tool: waste_detection"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_waste_detection(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="waste_detection",
                description="Waste Detection - Part of AWS Cost Optimizer",
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
        if name == "waste_detection":
            # TODO: Implement waste_detection
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "waste_detection"}  ))]
