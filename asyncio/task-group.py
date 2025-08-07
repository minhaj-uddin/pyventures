import random
import asyncio


class DownloadManager:
    def __init__(self, max_concurrent_downloads=3, timeout=4, max_retries=2):
        self.download_queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(max_concurrent_downloads)
        self.lock = asyncio.Lock()
        self.completed = 0
        self.timeout = timeout
        self.max_retries = max_retries

    async def _simulate_download(self, file_id: str):
        print(f"[START] Downloading {file_id}")
        delay = random.uniform(1, 5)
        await asyncio.sleep(delay)
        if random.random() < 0.3:
            raise Exception(f"Simulated error for {file_id}")
        print(f"[DONE]  Downloaded {file_id}")

        # Update shared state safely
        async with self.lock:
            self.completed += 1
            print(f"[✅] Completed {self.completed} downloads.")

    async def download_file(self, file_id: str):
        async with self.semaphore:
            try:
                await asyncio.wait_for(self._simulate_download(file_id), timeout=self.timeout)
            except asyncio.TimeoutError:
                raise Exception(f"Timeout while downloading {file_id}")
            except Exception as e:
                raise e

    async def _attempt_with_retries(self, file_id):
        for attempt in range(1, self.max_retries + 2):
            try:
                await self.download_file(file_id)
                return
            except Exception as e:
                print(f"[RETRY {attempt}] Failed to download {file_id}: {e}")
                if attempt <= self.max_retries:
                    await asyncio.sleep(1 * attempt)
                else:
                    print(
                        f"[ERROR] Giving up on {file_id} after {self.max_retries} retries.")

    async def worker(self, name: str):
        while True:
            file_id = await self.download_queue.get()
            print(f"[{name}] Picked up {file_id}")
            try:
                await self._attempt_with_retries(file_id)
            finally:
                self.download_queue.task_done()

    async def run(self, files: list[str], num_workers=5):
        # Populate the queue
        for f in files:
            await self.download_queue.put(f)

        # Launch workers using TaskGroup
        async with asyncio.TaskGroup() as tg:
            for i in range(num_workers):
                tg.create_task(self.worker(f"Worker-{i+1}"))

        print("\n✅ All downloads completed or failed after retries.")


if __name__ == "__main__":
    files_to_download = [f"file-{i}" for i in range(1, 11)]

    async def main():
        try:
            manager = DownloadManager(
                max_concurrent_downloads=3,
                timeout=4,
                max_retries=2
            )
            await manager.run(files_to_download)
        except asyncio.CancelledError:
            print(f"[ERROR] - Task was cancelled.")

    asyncio.run(main())
