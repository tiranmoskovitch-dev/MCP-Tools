"""Tool: news_sentiment"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_news_sentiment(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="news_sentiment",
                description="News Sentiment - Part of Stock Sentiment Analyzer",
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
        if name == "news_sentiment":
            # TODO: Implement news_sentiment
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "news_sentiment"}  ))]
