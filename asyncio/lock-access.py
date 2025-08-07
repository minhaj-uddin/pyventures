import asyncio

counter = 0
lock = asyncio.Lock()


async def safe_increment(name):
    global counter
    for _ in range(5):
        async with lock:
            old = counter
            await asyncio.sleep(0.1)
            counter = old + 1
            print(f"{name}: counter = {counter}")


async def main():
    await asyncio.gather(
        safe_increment("Task-1"),
        safe_increment("Task-2"),
    )

asyncio.run(main())
