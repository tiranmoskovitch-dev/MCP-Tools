"""MCP Server: Full SIEM Log Platform
Threat detection, incident response, forensics, correlation rules
Price: $149
"""
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools.ingest_logs import register_ingest_logs
from src.tools.detect_threats import register_detect_threats
from src.tools.correlate_events import register_correlate_events
from src.tools.incident_timeline import register_incident_timeline
from src.tools.forensic_analysis import register_forensic_analysis
from src.tools.alert_rules import register_alert_rules
from src.tools.dashboard_data import register_dashboard_data

server = Server("mcp-siem")


def register_all_tools():
    register_ingest_logs(server)
    register_detect_threats(server)
    register_correlate_events(server)
    register_incident_timeline(server)
    register_forensic_analysis(server)
    register_alert_rules(server)
    register_dashboard_data(server)


async def run():
    register_all_tools()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
