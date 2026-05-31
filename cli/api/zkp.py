"""
cli/api/zkp.py — Zero-knowledge KYC credentials.

Endpoints (prefix /api/v1/zkp):
  POST  /setup-key
  POST  /verify
  GET   /status
  POST  /revoke/{credential_id}
"""
from __future__ import annotations

from typing import Any

from cli.http import request
from cli.settings import settings


def _u(path: str = "") -> str:
    return f"{settings.api_url}/zkp{path}"


async def setup_key(payload: dict[str, Any]) -> dict[str, Any]:
    return (await request("POST", _u("/setup-key"), json=payload)).json()


async def verify(payload: dict[str, Any]) -> dict[str, Any]:
    return (await request("POST", _u("/verify"), json=payload)).json()


async def status() -> dict[str, Any]:
    return (await request(
        "GET", _u("/status"),
        cache_key="zkp:status", cache_ttl=60.0,
    )).json()


async def revoke(credential_id: str) -> dict[str, Any]:
    return (await request("POST", _u(f"/revoke/{credential_id}"))).json()
