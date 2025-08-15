import uuid
from aiohttp import web

APP_VERSION = "1.2.0"


# Request handler
async def handle(request):
    return web.Response(text="Hello, World!")


# Signal callback: add headers before sending response
async def add_custom_headers(request, response):
    # Unique request ID
    request_id = str(uuid.uuid4())

    # Add custom headers
    response.headers["X-App-Version"] = APP_VERSION
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"

    print(f"→ Added headers to response for {request.method} {request.path}")
    print(f"→ Response Headers: {response.headers}")

# App setup
app = web.Application()

# Register signal handler
app.on_response_prepare.append(add_custom_headers)

# Route
app.router.add_get('/', handle)

# Run the app
# curl -i http://localhost:8080/
web.run_app(app)
