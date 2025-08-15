import time
from aiohttp import web


# Middleware for logging
@web.middleware
async def logging_middleware(request, handler):
    start_time = time.time()
    print(f"--> Request started: {request.method} {request.path}")

    try:
        response = await handler(request)
    except Exception as e:
        print(f"!! Exception occurred: {e}")
        raise
    finally:
        duration = time.time() - start_time
        print(
            f"<-- Request finished: {request.method} {request.path} in {duration:.2f}s")

    return response


async def handle(request):
    return web.Response(text="Hello, world!")

# App setup
app = web.Application(middlewares=[logging_middleware])
app.router.add_get('/', handle)


# Signal handlers for startup and cleanup
async def on_startup(app):
    print("🚀 App is starting...")


async def on_cleanup(app):
    print("🧹 App is cleaning up...")

app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

# Run the app
web.run_app(app)
