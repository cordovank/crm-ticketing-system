"""
Auth middleware to extract and verify tokens from incoming requests.
Attaches the user role to request.state.role for downstream handlers.
Also logs request processing time in X-Process-Time-ms header.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time

from app.auth.tokens import get_role_from_token


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()

        # ------------------
        # AUTHENTICATION
        # ------------------
        auth_header = request.headers.get("Authorization")
        role = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            role = get_role_from_token(token)

        request.state.role = role  # None if unauthenticated

        # ------------------
        # PROCESS REQUEST
        # ------------------
        response = await call_next(request)

        # ------------------
        # LOGGING
        # ------------------
        duration = round((time.time() - start) * 1000, 2)
        response.headers["X-Process-Time-ms"] = str(duration)

        return response
