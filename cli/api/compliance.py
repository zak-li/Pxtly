"""
cli/api/compliance.py — KYC / AML / sanctions workflows.

Endpoints (prefix /api/v1/compliance):
  GET   ""                          (compliance dashboard summary)
  GET   /alerts/active
  GET   /{user_id}                  (per-user status)
  POST  /kyc/submit
  POST  /kyc/approve
  POST  /screening/run
"""
from __future__ import annotations

from typing import Any

from cli.http import request
from cli.settings import settings


def _u(path: str = "") -> str:
    return f"{settings.api_url}/compliance{path}"


async def summary() -> dict[str, Any]:
    return (await request(
        "GET", _u(""),
        cache_key="compliance:summary", cache_ttl=60.0,
    )).json()


async def alerts() -> list[dict[str, Any]]:
    return (await request(
        "GET", _u("/alerts/active"),
        cache_key="compliance:alerts", cache_ttl=30.0,
    )).json()


async def user_status(user_id: str) -> dict[str, Any]:
    return (await request("GET", _u(f"/{user_id}"))).json()


async def kyc_submit(payload: dict[str, Any]) -> dict[str, Any]:
    return (await request("POST", _u("/kyc/submit"), json=payload)).json()


async def kyc_approve(payload: dict[str, Any]) -> dict[str, Any]:
    return (await request("POST", _u("/kyc/approve"), json=payload)).json()


async def screening_run(payload: dict[str, Any]) -> dict[str, Any]:
    return (await request("POST", _u("/screening/run"), json=payload)).json()
