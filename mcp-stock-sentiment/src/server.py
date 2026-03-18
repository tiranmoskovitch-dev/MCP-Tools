"""MCP Server: Stock Sentiment Analyzer
Earnings call NLP, insider trades, options flow, SEC filing parser
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.analyze_earnings import register_analyze_earnings
from src.tools.insider_trades import register_insider_trades
from src.tools.options_flow import register_options_flow
from src.tools.sec_filings import register_sec_filings
from src.tools.news_sentiment import register_news_sentiment
from src.tools.analyst_ratings import register_analyst_ratings

server = Server("mcp-stock-sentiment")


def register_all_tools():
    register_analyze_earnings(server)
    register_insider_trades(server)
    register_options_flow(server)
    register_sec_filings(server)
    register_news_sentiment(server)
    register_analyst_ratings(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
