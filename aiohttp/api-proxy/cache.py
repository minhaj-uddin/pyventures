from aiohttp_cache import setup_cache, cache


def setup_cache_decorator(app):
    setup_cache(app)


cache_response = cache(expires=600)
