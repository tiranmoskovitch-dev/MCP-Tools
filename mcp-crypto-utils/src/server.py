"""MCP Server: Hash & Crypto Utilities
Hash files, JWT decode/verify, base64, encryption helpers
Price: $29
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.hash_text import register_hash_text
from src.tools.hash_file import register_hash_file
from src.tools.jwt_decode import register_jwt_decode
from src.tools.jwt_verify import register_jwt_verify
from src.tools.base64_encode import register_base64_encode
from src.tools.encrypt_aes import register_encrypt_aes
from src.tools.generate_key import register_generate_key

server = Server("mcp-crypto-utils")


def register_all_tools():
    register_hash_text(server)
    register_hash_file(server)
    register_jwt_decode(server)
    register_jwt_verify(server)
    register_base64_encode(server)
    register_encrypt_aes(server)
    register_generate_key(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
