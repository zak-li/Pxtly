"""
cli/security/
-------------
Security primitives for the Pxtly CLI:

  - tokens : keyring-backed token store with access+refresh+expiry
  - pkce   : OAuth 2.0 Authorization Code + PKCE helpers (RFC 7636)
  - audit  : append-only local audit log for executed commands
"""
from __future__ import annotations

from cli.security.audit import audit_event, recent_events
from cli.security.pkce import (
    build_authorization_url,
    generate_pkce_pair,
    generate_state,
)
from cli.security.tokens import (
    TokenBundle,
    delete_tokens,
    get_access_token,
    get_token_bundle,
    has_tokens,
    save_token_bundle,
)

__all__ = [
    "TokenBundle",
    "audit_event",
    "build_authorization_url",
    "delete_tokens",
    "generate_pkce_pair",
    "generate_state",
    "get_access_token",
    "get_token_bundle",
    "has_tokens",
    "recent_events",
    "save_token_bundle",
]
