from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from app.core.config import settings


def hash_password(password: str, *, salt: str | None = None) -> str:
    resolved_salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), resolved_salt.encode("utf-8"), 200_000)
    encoded = base64.b64encode(digest).decode("utf-8")
    return f"{resolved_salt}${encoded}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, expected_hash = stored_hash.split("$", maxsplit=1)
    except ValueError:
        return False
    recomputed = hash_password(password, salt=salt).split("$", maxsplit=1)[1]
    return hmac.compare_digest(recomputed, expected_hash)


def new_session_token() -> str:
    return secrets.token_urlsafe(32)


def session_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=settings.session_ttl_days)
