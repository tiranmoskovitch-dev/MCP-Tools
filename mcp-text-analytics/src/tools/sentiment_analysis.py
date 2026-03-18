"""Tool: sentiment_analysis"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_sentiment_analysis(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="sentiment_analysis",
                description="Sentiment Analysis - Part of Text Analytics",
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
        if name == "sentiment_analysis":
            # TODO: Implement sentiment_analysis
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "sentiment_analysis"}  ))]
