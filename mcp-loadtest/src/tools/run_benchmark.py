"""Tool: run_benchmark"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import json


def register_run_benchmark(server: Server):
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="run_benchmark",
                description="Run Benchmark - Part of API Load Tester",
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
        if name == "run_benchmark":
            # TODO: Implement run_benchmark
            return [TextContent(type="text", text=json.dumps({"status": "not_implemented", "tool": "run_benchmark"}  ))]
