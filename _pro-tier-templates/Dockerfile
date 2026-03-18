# Multi-stage Dockerfile for MCP server deployment
# Works with any mcp-* tool — pass TOOL_NAME at build time
#
# Build:
#   docker build --build-arg TOOL_NAME=mcp-dns-intel -t mcp-dns-intel .
#
# Run:
#   docker run --rm -i mcp-dns-intel

# ── Stage 1: Build ──────────────────────────────────────────────
FROM python:3.11-slim AS builder

ARG TOOL_NAME
RUN test -n "$TOOL_NAME" || (echo "ERROR: TOOL_NAME build arg is required" && exit 1)

WORKDIR /build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/

# Build a wheel for clean installation
RUN pip install --no-cache-dir build && \
    python -m build --wheel --outdir /build/dist

# ── Stage 2: Runtime ────────────────────────────────────────────
FROM python:3.11-slim AS runtime

ARG TOOL_NAME

# Security: run as non-root
RUN groupadd --gid 1000 mcpuser && \
    useradd --uid 1000 --gid 1000 --create-home mcpuser

WORKDIR /app

# Install the built wheel
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm -f /tmp/*.whl

# Create config directory for volume mount
RUN mkdir -p /app/config && chown mcpuser:mcpuser /app/config

# Store tool name for the entrypoint
RUN echo "$TOOL_NAME" > /app/.tool_name

# Health check script
COPY --chown=mcpuser:mcpuser <<'HEALTHCHECK' /app/healthcheck.py
"""Health check: verify the MCP server module can be imported."""
import sys
try:
    import src.server
    sys.exit(0)
except Exception as e:
    print(f"Health check failed: {e}", file=sys.stderr)
    sys.exit(1)
HEALTHCHECK

USER mcpuser

# MCP servers communicate over stdio
# The entrypoint runs the console_scripts entry point installed from pyproject.toml
ENTRYPOINT ["sh", "-c", "exec $(cat /app/.tool_name)"]
