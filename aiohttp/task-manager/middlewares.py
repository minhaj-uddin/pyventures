import time
from aiohttp import web


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:
        return web.json_response({'error': ex.reason}, status=ex.status)
    except Exception as e:
        return web.json_response({'error': {e}}, status=500)


@web.middleware
async def logging_middleware(request, handler):
    start = time.time()
    response = await handler(request)
    duration = time.time() - start
    print(f"{request.method} {request.path} -> {response.status} ({duration:.3f}s)")
    return response
