"""MCP Server: Text Analytics
Readability score, keyword density, sentiment, language detection
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.readability_score import register_readability_score
from src.tools.keyword_density import register_keyword_density
from src.tools.detect_language import register_detect_language
from src.tools.sentiment_analysis import register_sentiment_analysis
from src.tools.word_frequency import register_word_frequency
from src.tools.summarize import register_summarize

server = Server("mcp-text-analytics")


def register_all_tools():
    register_readability_score(server)
    register_keyword_density(server)
    register_detect_language(server)
    register_sentiment_analysis(server)
    register_word_frequency(server)
    register_summarize(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
