import jwt
from aiohttp import web

# Dummy secret and roles
SECRET = "super-secret"
USER_ROLES = {"alice": "doctor", "bob": "nurse"}


def verify_jwt(request):
    auth = request.headers.get("Authorization", "")
    token = auth.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload.get("sub"), USER_ROLES.get(payload.get("sub"))
    except Exception as exc:
        raise web.HTTPUnauthorized(text=f"Invalid token: {exec}") from exc


def require_roles(*roles):
    async def middleware(request, handler):
        user, role = verify_jwt(request)
        if role not in roles:
            raise web.HTTPForbidden(text="Access denied")
        request["user"] = user
        request["role"] = role
        return await handler(request)
    return middleware
