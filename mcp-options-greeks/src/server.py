"""MCP Server: Options Greeks Calculator
Black-Scholes, IV surface, strategy builder, risk scenarios
Price: $79
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.calculate_greeks import register_calculate_greeks
from src.tools.iv_surface import register_iv_surface
from src.tools.build_strategy import register_build_strategy
from src.tools.risk_scenario import register_risk_scenario
from src.tools.payoff_diagram import register_payoff_diagram
from src.tools.optimal_strike import register_optimal_strike

server = Server("mcp-options-greeks")


def register_all_tools():
    register_calculate_greeks(server)
    register_iv_surface(server)
    register_build_strategy(server)
    register_risk_scenario(server)
    register_payoff_diagram(server)
    register_optimal_strike(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
