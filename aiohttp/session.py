import time
import base64
from aiohttp import web
from cryptography import fernet
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage


async def handler(request):
    session = await get_session(request)

    last_visit = session.get("last_visit")
    session["last_visit"] = time.time()
    text = f"Last visited: {last_visit}"

    return web.Response(text=text)


async def make_app():
    app = web.Application()
    # secret_key: 32 base64-encoded bytes
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    app.add_routes([web.get('/', handler)])
    return app

web.run_app(make_app())
