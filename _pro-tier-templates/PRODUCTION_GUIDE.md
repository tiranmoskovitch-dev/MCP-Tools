# Production Deployment Guide

How to deploy an MCP server tool in a production environment.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Docker Deployment](#docker-deployment)
3. [Systemd Service (Bare Metal)](#systemd-service-bare-metal)
4. [Environment Variables](#environment-variables)
5. [Rate Limiting](#rate-limiting)
6. [Health Checks and Monitoring](#health-checks-and-monitoring)
7. [Security Best Practices](#security-best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.10+ (3.11 recommended)
- Docker 24+ and Docker Compose v2 (for container deployments)
- Linux host recommended for production (Ubuntu 22.04+ or Debian 12+)

---

## Docker Deployment

### Quick Start

1. Copy `Dockerfile` and `docker-compose.yml` into your `mcp-<name>/` directory.

2. Create a `.env` file:

```bash
TOOL_NAME=mcp-dns-intel
MCP_LOG_LEVEL=INFO
```

3. Build and run:

```bash
docker compose build
docker compose up -d
```

4. Verify the container is healthy:

```bash
docker compose ps
docker compose logs --tail=20
```

### Custom Configuration

Create a `config/` directory in the tool root. Mount it as a read-only volume (already configured in docker-compose.yml). Place any configuration files there — the server can read them from `/app/config/` inside the container.

### Updating

```bash
docker compose pull    # if using a registry
docker compose build   # if building locally
docker compose up -d   # recreates the container with zero downtime
```

---

## Systemd Service (Bare Metal)

For deployments without Docker, run the MCP server as a systemd service.

### 1. Install the package

```bash
cd /opt/mcp-tools/mcp-dns-intel
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### 2. Create the service file

Save as `/etc/systemd/system/mcp-dns-intel.service`:

```ini
[Unit]
Description=MCP Server: mcp-dns-intel
After=network.target
Documentation=https://github.com/your-org/mcp-dns-intel

[Service]
Type=simple
User=mcp
Group=mcp
WorkingDirectory=/opt/mcp-tools/mcp-dns-intel
ExecStart=/opt/mcp-tools/mcp-dns-intel/.venv/bin/mcp-dns-intel
Restart=on-failure
RestartSec=5
StartLimitBurst=5
StartLimitIntervalSec=60

# Environment
Environment=MCP_LOG_LEVEL=INFO
EnvironmentFile=-/opt/mcp-tools/mcp-dns-intel/.env

# Security hardening
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
RestrictSUIDSGID=yes
RestrictNamespaces=yes
ReadWritePaths=/opt/mcp-tools/mcp-dns-intel/config

# Resource limits
MemoryMax=512M
CPUQuota=100%
TasksMax=64

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mcp-dns-intel

[Install]
WantedBy=multi-user.target
```

### 3. Create the service user

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin mcp
sudo chown -R mcp:mcp /opt/mcp-tools/mcp-dns-intel
```

### 4. Enable and start

```bash
sudo systemctl daemon-reload
sudo systemctl enable mcp-dns-intel
sudo systemctl start mcp-dns-intel
sudo systemctl status mcp-dns-intel
```

### 5. View logs

```bash
journalctl -u mcp-dns-intel -f
journalctl -u mcp-dns-intel --since "1 hour ago"
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `MCP_LOG_LEVEL` | `INFO` | Logging level: DEBUG, INFO, WARNING, ERROR |
| `MCP_CONFIG_PATH` | `./config` | Path to configuration directory |
| `MCP_RATE_LIMIT_RPM` | `60` | Requests per minute (rate limiter) |
| `MCP_RATE_LIMIT_BURST` | Same as RPM | Maximum burst size |

Tool-specific variables should be documented in the tool's own README. Set them in `.env` (Docker) or the `EnvironmentFile` (systemd).

---

## Rate Limiting

The included `rate_limiter.py` module provides token bucket rate limiting.

### Per-tool limiting (decorator)

```python
from rate_limiter import rate_limit

@rate_limit(rpm=30)
async def whois_lookup(domain: str) -> dict:
    ...
```

### Global limiting (all tools share one pool)

```python
from rate_limiter import RateLimiter, RateLimitExceeded

limiter = RateLimiter(rpm=120, burst=20)

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None):
    if not limiter.allow(name):
        retry = limiter.retry_after(name)
        return [TextContent(
            type="text",
            text=json.dumps({"error": "rate_limited", "retry_after_seconds": round(retry, 1)})
        )]
    # ... dispatch to handler
```

### Configuration via environment

```python
import os
from rate_limiter import RateLimiter

limiter = RateLimiter(
    rpm=int(os.environ.get("MCP_RATE_LIMIT_RPM", "60")),
    burst=int(os.environ.get("MCP_RATE_LIMIT_BURST", "60")),
)
```

---

## Health Checks and Monitoring

### Docker health check

Already configured in `docker-compose.yml`. The health check verifies the server module can be imported. Check status with:

```bash
docker inspect --format='{{.State.Health.Status}}' mcp-dns-intel
```

### HTTP health endpoint (optional)

If you need an HTTP health endpoint for a load balancer or monitoring system, run a lightweight sidecar:

```python
"""Save as healthcheck_http.py and run alongside the MCP server."""
import http.server
import importlib
import sys

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            try:
                importlib.import_module("src.server")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status":"healthy"}')
            except Exception as e:
                self.send_response(503)
                self.end_headers()
                self.wfile.write(f'{{"status":"unhealthy","error":"{e}"}}'.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # suppress access logs

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = http.server.HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health check listening on :{port}/health")
    server.serve_forever()
```

### Monitoring checklist

- **Process alive**: systemd or Docker restart policy handles this automatically.
- **Memory usage**: Set limits (512M in both systemd and Docker configs). Alert at 80%.
- **Log errors**: Pipe `journalctl` or Docker logs to your log aggregator. Alert on `"error"` in JSON output.
- **Rate limit hits**: The rate limiter raises `RateLimitExceeded` — log these to track demand.

---

## Security Best Practices

### 1. Run as non-root

Both the Dockerfile and systemd service file create and use a dedicated `mcp` / `mcpuser` user with minimal privileges.

### 2. API keys and secrets

Never hardcode secrets in source code. Use environment variables or mounted secret files:

```bash
# Docker: pass secrets via environment
docker run -e API_KEY_FILE=/run/secrets/api_key ...

# Systemd: use EnvironmentFile
EnvironmentFile=/opt/mcp-tools/mcp-dns-intel/.env
```

Restrict permissions on secret files:

```bash
chmod 600 /opt/mcp-tools/mcp-dns-intel/.env
chown mcp:mcp /opt/mcp-tools/mcp-dns-intel/.env
```

### 3. Network isolation

MCP servers communicate over stdio, not over the network. This is a security advantage — there is no open port to attack.

For additional isolation in Docker:

```yaml
# Add to docker-compose.yml service
network_mode: "none"  # no network access at all
```

Only enable networking if the tool needs to make outbound requests (DNS lookups, API calls, etc.).

### 4. Read-only filesystem

The Docker Compose config sets `read_only: true` with a tmpfs for `/tmp`. The systemd service uses `ProtectSystem=strict`. This prevents an attacker from modifying binaries or configs at runtime.

### 5. Resource limits

Both deployment methods cap memory at 512M and CPU at 100% of one core. Adjust based on your workload, but always set limits to prevent runaway processes from affecting the host.

### 6. Dependency auditing

Run regular vulnerability scans:

```bash
pip install pip-audit
pip-audit
```

Pin dependency versions in `pyproject.toml` for reproducible builds. Update dependencies on a regular schedule.

### 7. Logging

- Log all tool invocations with timestamps (but not sensitive input data).
- Ship logs to a centralized system (ELK, Loki, CloudWatch, etc.).
- Set up alerts for unusual patterns: error spikes, rate limit bursts, unexpected tool names.

---

## Troubleshooting

### Container exits immediately

MCP servers expect stdin to remain open. Ensure `stdin_open: true` is set in docker-compose.yml. If running manually:

```bash
docker run --rm -i mcp-dns-intel  # -i keeps stdin open
```

### "Module not found" errors

Verify the package installed correctly inside the container:

```bash
docker run --rm --entrypoint pip mcp-dns-intel list | grep mcp
```

### Rate limiter too aggressive

Increase the RPM or burst values. The rate limiter uses in-memory state, so restarting the server resets all counters.

### Systemd service won't start

Check permissions and paths:

```bash
sudo -u mcp /opt/mcp-tools/mcp-dns-intel/.venv/bin/mcp-dns-intel
```

If this works but systemd doesn't, check `journalctl -u mcp-dns-intel` for sandboxing errors.
