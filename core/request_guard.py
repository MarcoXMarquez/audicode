# core/request_guard.py
# Cross-site / host-header protections and setup/admin loopback checks.

import hmac
import ipaddress
import os
from urllib.parse import urlsplit

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
FORWARD_HEADERS = ("x-forwarded-for", "x-forwarded-host", "x-real-ip", "forwarded")
LOOPBACK_BINDS = {"127.0.0.1", "::1", "localhost"}


def parse_allowed_origins(raw: str) -> list:
    return [o.strip().rstrip("/") for o in raw.split(",") if o.strip()]


def is_loopback_host(host) -> bool:
    if not host:
        return False
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def is_private_host(host) -> bool:
    try:
        return ipaddress.ip_address(host).is_private
    except (ValueError, TypeError):
        return False


def has_forward_headers(request: Request) -> bool:
    return any(h in request.headers for h in FORWARD_HEADERS)


def is_direct_loopback(request: Request) -> bool:
    """Client connected straight from loopback, not through a reverse proxy."""
    client = request.client.host if request.client else None
    return is_loopback_host(client) and not has_forward_headers(request)


def assert_safe_bind(auth_enabled: bool, bind: str) -> None:
    """Refuse to run without auth on a non-loopback interface."""
    if not auth_enabled and bind not in LOOPBACK_BINDS:
        raise RuntimeError(
            f"Refusing to start: AUTH_ENABLED=false with APP_BIND={bind}. "
            "Disabling auth is only allowed on loopback (127.0.0.1)."
        )


def check_setup_allowed(request: Request) -> None:
    """Gate first-run admin creation so a port scanner can't claim the instance.

    Allowed when AUDICODE_SETUP_TOKEN is set and matches X-Setup-Token, or,
    without a token, when the client is direct loopback. Docker setups publish
    on host loopback, where the container sees the bridge IP; they opt in with
    AUDICODE_SETUP_ALLOW_PRIVATE=true (compose sets it).
    """
    token = os.getenv("AUDICODE_SETUP_TOKEN", "")
    if token:
        supplied = request.headers.get("x-setup-token", "")
        if hmac.compare_digest(supplied, token):
            return
        raise HTTPException(403, "Setup token required (X-Setup-Token header)")
    if is_direct_loopback(request):
        return
    client = request.client.host if request.client else None
    if (os.getenv("AUDICODE_SETUP_ALLOW_PRIVATE", "false").lower() == "true"
            and is_private_host(client) and not has_forward_headers(request)):
        return
    raise HTTPException(
        403,
        "Initial setup is only allowed from the local machine. Open the app via "
        "127.0.0.1, or set AUDICODE_SETUP_TOKEN and send it as X-Setup-Token.",
    )


class OriginGuardMiddleware(BaseHTTPMiddleware):
    """Reject state-changing requests whose Origin is neither same-host nor allowed.

    Non-browser clients send no Origin and pass through; browsers always send it
    on cross-site POST/PUT/PATCH/DELETE, which blocks CSRF on form-encoded routes.
    """

    def __init__(self, app, allowed_origins):
        super().__init__(app)
        self.allowed = {o.lower() for o in allowed_origins}

    async def dispatch(self, request: Request, call_next):
        if request.method in UNSAFE_METHODS:
            origin = request.headers.get("origin")
            if origin and origin != "null":
                o = origin.rstrip("/").lower()
                host = request.headers.get("host", "").lower()
                if o not in self.allowed and urlsplit(o).netloc != host:
                    return JSONResponse({"detail": "Cross-origin request blocked"}, status_code=403)
            elif origin == "null":
                return JSONResponse({"detail": "Cross-origin request blocked"}, status_code=403)
        return await call_next(request)
