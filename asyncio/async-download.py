import random
import asyncio


class DownloadManager:
    def __init__(self, max_concurrent_downloads=3):
        self.download_queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(max_concurrent_downloads)
        self.lock = asyncio.Lock()
        self.completed = 0

    async def download_file(self, file_id: str):
        # Use semaphore to limit concurrency
        async with self.semaphore:
            print(f"[START] Downloading {file_id}")
            await asyncio.sleep(random.uniform(1, 3))
            print(f"[DONE]  Downloaded {file_id}")

            # Update shared counter safely
            async with self.lock:
                self.completed += 1
                print(f"[PROGRESS] Completed {self.completed} downloads.")

    async def worker(self, name: str):
        while True:
            file_id = await self.download_queue.get()
            print(f"[{name}] Picked up {file_id}")
            try:
                await self.download_file(file_id)
            finally:
                self.download_queue.task_done()

    async def main(self, files: list[str], num_workers=5):
        # Enqueue files
        for f in files:
            await self.download_queue.put(f)

        # Start worker pool
        workers = [asyncio.create_task(self.worker(f"Worker-{i+1}"))
                   for i in range(num_workers)]

        # Wait for all tasks to be processed
        await self.download_queue.join()

        # Cancel workers (they loop forever)
        for w in workers:
            w.cancel()

        print("\n✅ All downloads complete.")


if __name__ == "__main__":
    files_to_download = [f"file-{i}" for i in range(1, 11)]

    async def run():
        manager = DownloadManager(max_concurrent_downloads=3)
        await manager.main(files_to_download, num_workers=5)

    asyncio.run(run())
