"""MCP Server: Log Analyzer & Parser
Parse any log format, pattern detection, error clustering
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.parse_log import register_parse_log
from src.tools.detect_patterns import register_detect_patterns
from src.tools.cluster_errors import register_cluster_errors
from src.tools.timeline_analysis import register_timeline_analysis
from src.tools.extract_metrics import register_extract_metrics
from src.tools.alert_rules import register_alert_rules

server = Server("mcp-log-analyzer")


def register_all_tools():
    register_parse_log(server)
    register_detect_patterns(server)
    register_cluster_errors(server)
    register_timeline_analysis(server)
    register_extract_metrics(server)
    register_alert_rules(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
