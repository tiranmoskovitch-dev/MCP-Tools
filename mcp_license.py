"""
MCP Tools License Gate - shared across all MCP servers.
Each server defines its free tools. The rest require a license.

Usage in server.py:
    from mcp_license import check_tool_access, get_status_text

    # In the tool handler:
    if not check_tool_access("mcp-qrcode", tool_name):
        return [TextContent(type="text", text=get_blocked_text("mcp-qrcode", tool_name))]
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path

TRIAL_DAYS = 7
STORE_URL = "https://whop.com/mcp-tools/"

# First 2 tools in each server are free. Rest require pro.
FREE_TOOLS = {
    "mcp-dns-intel": {"whois_lookup", "dns_records"},
    "mcp-email-deliverability": {"check_deliverability"},
    "mcp-image-tools": {"resize_image", "convert_format"},
    "mcp-pdf-toolkit": {"merge_pdfs", "extract_text"},
    "mcp-qrcode": {"generate_qr", "decode_qr"},
}


def _get_config(tool_name: str) -> dict:
    config_dir = Path.home() / ".mcp-tools"
    config_dir.mkdir(exist_ok=True)
    config_path = config_dir / f"{tool_name}.json"
    if config_path.exists():
        try:
            return json.loads(config_path.read_text())
        except Exception:
            pass
    config = {
        "installed": datetime.now().isoformat(),
        "license_key": "",
        "activated": False,
    }
    config_path.write_text(json.dumps(config, indent=2))
    return config


def _is_pro(server_name: str) -> bool:
    config = _get_config(server_name)
    if config.get("activated"):
        return True
    installed = datetime.fromisoformat(config["installed"])
    days_left = max(TRIAL_DAYS - (datetime.now() - installed).days, 0)
    return days_left > 0


def check_tool_access(server_name: str, tool_name: str) -> bool:
    """Check if a specific tool is accessible. Returns True if allowed."""
    free = FREE_TOOLS.get(server_name, set())
    if tool_name in free:
        return True
    return _is_pro(server_name)


def get_blocked_text(server_name: str, tool_name: str) -> str:
    free = FREE_TOOLS.get(server_name, set())
    return (
        f"'{tool_name}' is a Pro feature. "
        f"Free tools: {', '.join(sorted(free))}. "
        f"7-day trial expired. Upgrade at {STORE_URL}"
    )


def get_status_text(server_name: str) -> str:
    config = _get_config(server_name)
    if config.get("activated"):
        return "Pro (activated)"
    installed = datetime.fromisoformat(config["installed"])
    days = max(TRIAL_DAYS - (datetime.now() - installed).days, 0)
    if days > 0:
        return f"Trial ({days} days left)"
    return "Free tier"
