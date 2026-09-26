"""
FastAPI dependencies for authentication and role-based access control.
"""
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth0 import verify_token
from app.auth.models import TokenData

security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenData:
    """Extract and verify JWT from Authorization: Bearer <token> header."""
    if credentials is None:
        # No token provided — check if AUTH0_DOMAIN is set
        from app.core.config import settings
        if not settings.AUTH0_DOMAIN:
            # Demo mode — return admin
            return TokenData(
                sub="demo|admin",
                email="admin@demo.local",
                roles=["platform_admin"],
                team_id=None,
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return verify_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(allowed_roles: List[str]):
    """
    Factory that returns a FastAPI dependency enforcing role membership.
    Usage: Depends(require_roles(["platform_admin", "team_lead"]))
    """
    def _check(current_user: TokenData = Depends(get_current_user)) -> TokenData:
        for role in current_user.roles:
            if role in allowed_roles:
                return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. Required roles: {allowed_roles}",
        )
    return _check
