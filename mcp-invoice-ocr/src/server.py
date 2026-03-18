"""MCP Server: Invoice & Receipt OCR
Extract data from invoices/receipts, categorize expenses, export
Price: $49
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.extract_invoice import register_extract_invoice
from src.tools.extract_receipt import register_extract_receipt
from src.tools.categorize_expense import register_categorize_expense
from src.tools.batch_process import register_batch_process
from src.tools.export_csv import register_export_csv
from src.tools.tax_summary import register_tax_summary

server = Server("mcp-invoice-ocr")


def register_all_tools():
    register_extract_invoice(server)
    register_extract_receipt(server)
    register_categorize_expense(server)
    register_batch_process(server)
    register_export_csv(server)
    register_tax_summary(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
