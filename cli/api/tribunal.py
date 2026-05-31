"""
cli/api/tribunal.py — Regulator-side commit/reveal voting.

Endpoints (prefix /api/v1/tribunal):
  POST  /vote/commit
  POST  /vote/reveal
  POST  /session/{session_id}/tally
"""
from __future__ import annotations

from typing import Any

from cli.http import request
from cli.settings import settings


def _u(path: str = "") -> str:
    return f"{settings.api_url}/tribunal{path}"


async def vote_commit(payload: dict[str, Any]) -> dict[str, Any]:
    return (await request("POST", _u("/vote/commit"), json=payload)).json()


async def vote_reveal(payload: dict[str, Any]) -> dict[str, Any]:
    return (await request("POST", _u("/vote/reveal"), json=payload)).json()


async def tally(session_id: str) -> dict[str, Any]:
    return (await request("POST", _u(f"/session/{session_id}/tally"))).json()
