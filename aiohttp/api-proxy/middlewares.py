import time
from aiohttp import web


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:
        return web.json_response({"error": ex.reason}, status=ex.status)
    except Exception:
        return web.json_response({"error": "Internal Server Error"}, status=500)


@web.middleware
async def logging_middleware(request, handler):
    start = time.time()
    resp = await handler(request)
    duration = time.time() - start
    status = resp.status
    print(f"{request.method} {request.path} -> {status} in {duration:.3f}s")
    if 500 <= status < 600:
        # In real life, send metrics/alerts to monitoring service
        print(f"ALERT: 5xx spike? {status} at {request.path}")
    return resp
