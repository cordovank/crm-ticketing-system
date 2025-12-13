"""
Role-Based Access Control (RBAC) utilities.

Provides functions to enforce role requirements on API endpoints.
"""

from fastapi import Request, HTTPException


def require_role(request: Request, allowed_roles: list[str]):
    """
    Enforces that the role extracted by AuthMiddleware is in the allowed list.

    Example:
        require_role(request, ["admin"])
        require_role(request, ["agent", "admin"])
    """
    role = getattr(request.state, "role", None)

    if role not in allowed_roles:
        raise HTTPException(status_code=403, detail=f"Forbidden: role '{role}' unauthorized")
