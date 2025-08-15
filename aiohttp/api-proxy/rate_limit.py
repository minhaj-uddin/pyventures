from aiohttp_ratelimiter import Limiter, RateLimitMiddleware
from aiohttp_ratelimiter.backends.redis import RedisBackend
import aioredis

# Define Redis URL
REDIS_URL = "redis://localhost"


async def init_limiter(app):
    redis_pool = await aioredis.from_url(REDIS_URL, decode_responses=True)

    backend = RedisBackend(redis_pool)

    limiter = Limiter(backend=backend, default_limits=["100/1second"])

    app.middlewares.append(RateLimitMiddleware(limiter))
    app['rate_limiter'] = limiter
