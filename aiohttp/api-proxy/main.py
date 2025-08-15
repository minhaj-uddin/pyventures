from rate_limit import init_limiter
from middlewares import logging_middleware, error_middleware
from cache import setup_cache
from routes import routes
from aiohttp import web


async def create_app():
    app = web.Application(middlewares=[logging_middleware, error_middleware])

    setup_cache(app)
    await init_limiter(app)

    app.add_routes(routes)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)
