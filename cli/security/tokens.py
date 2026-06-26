"""
cli/security/tokens.py
----------------------
OS-keyring-backed token store for the Pxtly CLI.

Stores a full token bundle (access + refresh + expiry + scope) under a
single keyring entry so the CLI can:

  * detect expiry locally and pre-emptively refresh
  * fall back to refresh on a 401 from the API
  * clear everything on logout

There is intentionally NO file-based fallback. If the OS keyring is
unavailable, the CLI refuses to persist tokens — a deterministic failure
is safer than a "fallback" that pretends to be encrypted (the previous
XOR-on-username scheme was reversible by anyone who could read the file).
"""
from __future__ import annotations

import base64
import json
import logging
import time
from dataclasses import asdict, dataclass
from typing import Any

import keyring
import keyring.errors

log = logging.getLogger(__name__)

_SERVICE = "pxtly-cli"
_KEY = "session"
_CHUNK_SIZE = 500  # 500 chars = 1000 bytes in UTF-16. Windows CredWrite limit is 2560 bytes.

# JWTs frequently exceed the 1 KB Windows Credential Manager item limit when
# they carry roles / realm_access / scopes. Base64 the JSON bundle so the
# keyring backend just sees one opaque string of predictable shape.


@dataclass
class TokenBundle:
    """A full Keycloak/OIDC token bundle as persisted in the keyring."""

    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_at: float = 0.0  # absolute Unix epoch, NOT a relative duration
    refresh_expires_at: float = 0.0
    scope: str = ""

    # ── Lifecycle helpers ───────────────────────────────────────────────────

    @classmethod
    def from_oidc_response(cls, body: dict[str, Any]) -> TokenBundle:
        """Build a bundle from a raw Keycloak token endpoint response."""
        now = time.time()
        return cls(
            access_token=body["access_token"],
            refresh_token=body.get("refresh_token"),
            token_type=body.get("token_type", "Bearer"),
            expires_at=now + float(body.get("expires_in", 0)),
            refresh_expires_at=now + float(body.get("refresh_expires_in", 0)),
            scope=body.get("scope", ""),
        )

    def is_access_expired(self, leeway: float = 30.0) -> bool:
        """True if the access token has expired (or is within `leeway` seconds of it)."""
        if self.expires_at == 0:
            return False
        return time.time() >= (self.expires_at - leeway)

    def is_refresh_expired(self, leeway: float = 30.0) -> bool:
        if self.refresh_expires_at == 0 or not self.refresh_token:
            return True
        return time.time() >= (self.refresh_expires_at - leeway)

    def to_b64(self) -> str:
        return base64.urlsafe_b64encode(
            json.dumps(asdict(self)).encode("utf-8")
        ).decode("ascii")

    @classmethod
    def from_b64(cls, s: str) -> TokenBundle:
        return cls(**json.loads(base64.urlsafe_b64decode(s.encode("ascii"))))


# ── Public API ───────────────────────────────────────────────────────────────


def save_token_bundle(bundle: TokenBundle) -> None:
    """Persist the full bundle to the OS keyring."""
    try:
        raw = bundle.to_b64()
        chunks = [raw[i:i+_CHUNK_SIZE] for i in range(0, len(raw), _CHUNK_SIZE)]
        keyring.set_password(_SERVICE, f"{_KEY}_count", str(len(chunks)))
        for i, chunk in enumerate(chunks):
            keyring.set_password(_SERVICE, f"{_KEY}_{i}", chunk)
        log.debug("Token bundle saved in %d chunks (expires_at=%.0f).", len(chunks), bundle.expires_at)
    except keyring.errors.KeyringError as exc:
        raise RuntimeError(
            f"OS keyring is unavailable ({exc}). The Pxtly CLI requires a "
            "working keyring backend to store tokens securely. Install one "
            "of: Windows Credential Manager (built-in), macOS Keychain "
            "(built-in), or `pip install keyrings.cryptfile` on headless "
            "Linux."
        ) from exc


def get_token_bundle() -> TokenBundle | None:
    """Return the persisted bundle or None if nothing is stored."""
    try:
        count_str = keyring.get_password(_SERVICE, f"{_KEY}_count")
        if not count_str:
            return None
        count = int(count_str)
        raw = ""
        for i in range(count):
            chunk = keyring.get_password(_SERVICE, f"{_KEY}_{i}")
            if not chunk:
                return None
            raw += chunk
    except keyring.errors.KeyringError as exc:
        log.warning("Keyring read failed: %s", exc)
        return None
    except ValueError:
        return None

    if not raw:
        return None
    try:
        return TokenBundle.from_b64(raw)
    except Exception as exc:
        log.warning("Stored token bundle is corrupt (%s) — discarding.", exc)
        delete_tokens()
        return None


def get_access_token() -> str | None:
    """Return just the access token, or None. Does NOT refresh."""
    bundle = get_token_bundle()
    return bundle.access_token if bundle else None


def has_tokens() -> bool:
    return get_token_bundle() is not None


def delete_tokens() -> None:
    try:
        count_str = keyring.get_password(_SERVICE, f"{_KEY}_count")
        if count_str:
            count = int(count_str)
            for i in range(count):
                try:
                    keyring.delete_password(_SERVICE, f"{_KEY}_{i}")
                except keyring.errors.PasswordDeleteError:
                    pass
            keyring.delete_password(_SERVICE, f"{_KEY}_count")
        else:
            # Fallback to delete the old unchunked key if it exists
            keyring.delete_password(_SERVICE, _KEY)
        log.info("Token bundle cleared from keyring.")
    except keyring.errors.PasswordDeleteError:
        pass
    except keyring.errors.KeyringError as exc:
        log.warning("Keyring delete failed: %s", exc)

