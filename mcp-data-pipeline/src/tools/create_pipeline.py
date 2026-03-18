"""Tool: create_pipeline"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_create_pipeline(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="create_pipeline",
                description="Create Pipeline - Part of Data Pipeline Orchestrator",
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
        if name == "create_pipeline":
            # TODO: Implement create_pipeline
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "create_pipeline"}  ))]
