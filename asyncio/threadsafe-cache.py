import asyncio
from functools import wraps


def async_memoize():
    cache = {}
    in_flight = {}

    def decorator(func):
        @wraps(func)
        async def wrapper(*args):
            if args in cache:
                return cache[args]

            if args in in_flight:
                return await in_flight[args]

            task = asyncio.create_task(func(*args))
            in_flight[args] = task
            try:
                result = await task
                cache[args] = result
                return result
            finally:
                in_flight.pop(args, None)

        return wrapper
    return decorator


@async_memoize()
async def slow_api_call(x):
    print(f"Calling API with {x}...")
    await asyncio.sleep(2)
    return x * 10


async def main():
    print(await slow_api_call(5))  # First call: waits 2s
    print(await slow_api_call(5))  # Cached: returns instantly
    print(await slow_api_call(10))  # New input: waits 2s

if __name__ == "__main__":
    asyncio.run(main())
