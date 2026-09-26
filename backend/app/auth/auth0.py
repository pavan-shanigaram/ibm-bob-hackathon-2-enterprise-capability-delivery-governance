"""
Auth0 JWT verification using JWKS.
Fetches public keys from Auth0 and validates RS256-signed tokens.
"""
from typing import Optional
import httpx
from jose import jwt, JWTError
from app.core.config import settings
from app.auth.models import TokenData

_jwks_cache: Optional[dict] = None


def _get_jwks() -> dict:
    """Fetch JWKS from Auth0 (cached in-memory)."""
    global _jwks_cache
    if _jwks_cache is None:
        if not settings.AUTH0_DOMAIN:
            return {"keys": []}
        url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        _jwks_cache = response.json()
    return _jwks_cache


def verify_token(token: str) -> TokenData:
    """
    Verify an Auth0 JWT and return parsed token data.
    In dev/demo mode (no AUTH0_DOMAIN set), returns a mock admin token.
    """
    if not settings.AUTH0_DOMAIN:
        # Demo / dev mode — return a platform_admin token
        return TokenData(
            sub="demo|admin",
            email="admin@demo.local",
            roles=["platform_admin"],
            team_id=None,
        )

    try:
        jwks = _get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks.get("keys", []):
            if key.get("kid") == unverified_header.get("kid"):
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.AUTH0_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
        )

        roles = payload.get(f"{settings.AUTH0_NAMESPACE}roles", [])
        team_id = payload.get(f"{settings.AUTH0_NAMESPACE}team_id")

        return TokenData(
            sub=payload["sub"],
            email=payload.get("email"),
            roles=roles,
            team_id=int(team_id) if team_id else None,
        )
    except JWTError as exc:
        raise ValueError(f"Invalid token: {exc}") from exc
