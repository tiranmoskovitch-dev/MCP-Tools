"""Token bucket rate limiter for MCP server tools.

In-memory implementation with no external dependencies. Can be used as a
decorator on individual tool handlers or applied to the entire call_tool
dispatch.

Usage:
    from rate_limiter import RateLimiter, rate_limit

    # As a decorator — 30 requests per minute per tool
    @rate_limit(rpm=30)
    async def my_tool_handler(**kwargs):
        ...

    # As an instance for manual checking
    limiter = RateLimiter(rpm=60)
    if not limiter.allow("client_id"):
        raise RateLimitExceeded(limiter.retry_after("client_id"))
"""

from __future__ import annotations

import asyncio
import functools
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


class RateLimitExceeded(Exception):
    """Raised when a request exceeds the configured rate limit."""

    def __init__(self, retry_after: float):
        self.retry_after = retry_after
        super().__init__(
            f"Rate limit exceeded. Retry after {retry_after:.1f} seconds."
        )


@dataclass
class _Bucket:
    """Internal token bucket state for a single key."""
    tokens: float
    last_refill: float
    max_tokens: float
    refill_rate: float  # tokens per second

    def refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.max_tokens, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def consume(self, count: float = 1.0) -> bool:
        self.refill()
        if self.tokens >= count:
            self.tokens -= count
            return True
        return False

    def time_until_available(self, count: float = 1.0) -> float:
        self.refill()
        if self.tokens >= count:
            return 0.0
        deficit = count - self.tokens
        return deficit / self.refill_rate


@dataclass
class RateLimiter:
    """Token bucket rate limiter.

    Args:
        rpm: Maximum requests per minute. Tokens refill continuously.
        burst: Maximum burst size. Defaults to rpm (allows one minute of
               tokens to accumulate). Set lower to enforce stricter spacing.
    """
    rpm: int = 60
    burst: int | None = None
    _buckets: dict[str, _Bucket] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        if self.burst is None:
            self.burst = self.rpm

    def _get_bucket(self, key: str) -> _Bucket:
        if key not in self._buckets:
            max_tokens = float(self.burst)
            self._buckets[key] = _Bucket(
                tokens=max_tokens,
                last_refill=time.monotonic(),
                max_tokens=max_tokens,
                refill_rate=self.rpm / 60.0,
            )
        return self._buckets[key]

    def allow(self, key: str = "__global__", cost: float = 1.0) -> bool:
        """Check if a request is allowed and consume a token if so."""
        return self._get_bucket(key).consume(cost)

    def retry_after(self, key: str = "__global__", cost: float = 1.0) -> float:
        """Seconds until the next request would be allowed."""
        return self._get_bucket(key).time_until_available(cost)

    def reset(self, key: str | None = None) -> None:
        """Reset rate limit state. If key is None, reset all."""
        if key is None:
            self._buckets.clear()
        else:
            self._buckets.pop(key, None)

    def cleanup(self, max_idle_seconds: float = 3600.0) -> int:
        """Remove buckets that have been idle for too long. Returns count removed."""
        now = time.monotonic()
        stale = [
            k for k, b in self._buckets.items()
            if (now - b.last_refill) > max_idle_seconds
        ]
        for k in stale:
            del self._buckets[k]
        return len(stale)


# ── Global default limiter ──────────────────────────────────────

_default_limiter = RateLimiter(rpm=60)


def rate_limit(
    rpm: int = 60,
    burst: int | None = None,
    key_func: Callable[..., str] | None = None,
):
    """Decorator to rate-limit an async tool handler.

    Args:
        rpm: Requests per minute allowed.
        burst: Max burst tokens. Defaults to rpm.
        key_func: Optional callable(kwargs) -> str to extract a rate-limit
                  key (e.g., per-user limiting). Defaults to the function name.

    Raises:
        RateLimitExceeded: When the rate limit is exceeded, with retry_after
                           indicating how long to wait.

    Example:
        @rate_limit(rpm=30)
        async def whois_lookup(domain: str) -> dict:
            ...
    """
    limiter = RateLimiter(rpm=rpm, burst=burst)

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if key_func is not None:
                key = key_func(kwargs)
            else:
                key = func.__name__

            if not limiter.allow(key):
                raise RateLimitExceeded(limiter.retry_after(key))

            return await func(*args, **kwargs)

        # Expose the limiter for testing or manual control
        wrapper.limiter = limiter
        return wrapper

    return decorator


def apply_global_limit(
    handler_func,
    rpm: int = 60,
    burst: int | None = None,
):
    """Wrap an MCP call_tool handler with global rate limiting.

    This is meant to wrap the entire handle_call_tool dispatcher so all
    tool invocations share a single rate limit pool.

    Example:
        @server.call_tool()
        @apply_global_limit(rpm=120)
        async def handle_call_tool(name, arguments):
            ...
    """
    limiter = RateLimiter(rpm=rpm, burst=burst)

    @functools.wraps(handler_func)
    async def wrapper(*args, **kwargs):
        key = "__global__"
        if not limiter.allow(key):
            raise RateLimitExceeded(limiter.retry_after(key))
        return await handler_func(*args, **kwargs)

    wrapper.limiter = limiter
    return wrapper
