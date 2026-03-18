"""MCP Server: Git Repository Analyzer
Commit patterns, contributor stats, code churn, tech debt metrics
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.repo_summary import register_repo_summary
from src.tools.contributor_stats import register_contributor_stats
from src.tools.code_churn import register_code_churn
from src.tools.commit_patterns import register_commit_patterns
from src.tools.file_hotspots import register_file_hotspots
from src.tools.tech_debt_score import register_tech_debt_score

server = Server("mcp-git-analyzer")


def register_all_tools():
    register_repo_summary(server)
    register_contributor_stats(server)
    register_code_churn(server)
    register_commit_patterns(server)
    register_file_hotspots(server)
    register_tech_debt_score(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
