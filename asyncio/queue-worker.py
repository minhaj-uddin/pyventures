import random
import asyncio


async def producer(queue: asyncio.Queue, urls: list[str]):
    for url in urls:
        print(f"[Producer] Queueing URL: {url}")
        await queue.put(url)
    print("[Producer] Done adding URLs.")


async def worker(name: str, queue: asyncio.Queue):
    while True:
        url = await queue.get()
        print(f"[{name}] Fetching: {url}")
        await asyncio.sleep(random.uniform(1, 3))
        print(f"[{name}] Finished: {url}")
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    urls = [f"http://example.com/page{i}" for i in range(1, 11)]
    print(f"[Main] Total URLs to process: {len(urls)}")

    # Start producer task
    producer_task = asyncio.create_task(producer(queue, urls))

    # Start 3 workers
    workers = [asyncio.create_task(
        worker(f"Worker-{i+1}", queue)) for i in range(3)]

    # Wait until producer finishes
    await producer_task

    # Wait until all items in the queue are processed
    await queue.join()

    # Cancel workers since they loop forever
    for w in workers:
        w.cancel()

    print("All work completed.")

if __name__ == "__main__":
    asyncio.run(main())
