"""
cli/api/agent.py — MiCA regulatory RAG agent.

Endpoints (prefix /api/v1/agent):
  POST  /chat
  POST  /index            (re-index regulatory corpus, async 202)
  GET   /search
  GET   /status
"""
from __future__ import annotations

from typing import Any

from cli.http import request
from cli.settings import settings


def _u(path: str = "") -> str:
    return f"{settings.api_url}/agent{path}"


async def chat(message: str, stream: bool = False) -> dict[str, Any]:
    response = await request(
        "POST", _u("/chat"),
        json={"message": message, "stream": stream},
        cache_key=f"agent:chat:{hash(message)}", cache_ttl=300.0,
    )
    return response.json()


async def reindex() -> dict[str, Any]:
    return (await request("POST", _u("/index"))).json()


async def search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    return (await request(
        "GET", _u("/search"),
        params={"query": query, "top_k": top_k},
    )).json()


async def status() -> dict[str, Any]:
    return (await request(
        "GET", _u("/status"),
        cache_key="agent:status", cache_ttl=30.0,
    )).json()
