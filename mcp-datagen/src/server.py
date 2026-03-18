"""MCP Server: Lorem & Data Generator
Fake data generation: names, addresses, credit cards, UUIDs, datasets
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.fake_person import register_fake_person
from src.tools.fake_address import register_fake_address
from src.tools.fake_company import register_fake_company
from src.tools.fake_dataset import register_fake_dataset
from src.tools.generate_uuids import register_generate_uuids
from src.tools.fake_credit_card import register_fake_credit_card

server = Server("mcp-datagen")


def register_all_tools():
    register_fake_person(server)
    register_fake_address(server)
    register_fake_company(server)
    register_fake_dataset(server)
    register_generate_uuids(server)
    register_fake_credit_card(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
