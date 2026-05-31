"""
cli/api/system.py — Platform health probes.

Hits the unauthenticated /health and /health/deep endpoints exposed
directly at the API root (not under /api/v1).
"""
from __future__ import annotations

import logging
from typing import Any

import httpx

from cli.settings import settings

log = logging.getLogger(__name__)


def _root_url(path: str) -> str:
    """Strip /api/v1 from settings.api_url to hit the bare /health endpoint."""
    base = settings.api_url
    if base.endswith("/api/v1"):
        base = base[: -len("/api/v1")]
    return f"{base.rstrip('/')}{path}"


async def ping() -> tuple[bool, str]:
    """Return (is_up, message) — best-effort, no exceptions raised."""
    url = _root_url("/health")
    try:
        async with httpx.AsyncClient(
            verify=settings.verify_param, timeout=httpx.Timeout(5.0),
        ) as client:
            response = await client.get(url)
        if response.status_code == 200:
            return True, "Online"
        return False, f"HTTP {response.status_code}"
    except httpx.RequestError as exc:
        log.debug("Ping transport error: %s", exc)
        return False, str(exc)


async def deep_health() -> dict[str, Any]:
    """Readiness probe — checks Fabric, Vault, Neo4j connectivity."""
    url = _root_url("/health/deep")
    async with httpx.AsyncClient(
        verify=settings.verify_param, timeout=httpx.Timeout(15.0),
    ) as client:
        response = await client.get(url)
    return response.json()
