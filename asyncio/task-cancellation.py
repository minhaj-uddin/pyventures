import random
import asyncio


async def fetch_data(site: str):
    try:
        while True:
            print(f"[{site}] Fetching data...")
            await asyncio.sleep(random.uniform(1, 3))
            print(f"[{site}] Done.")
    except asyncio.CancelledError:
        print(f"[{site}] Cancelled. Cleaning up...")
        await asyncio.sleep(0.1)  # Simulate cleanup
        print(f"[{site}] Cleanup complete.")
        raise  # Important: re-raise to let gather() see the cancellation


async def main():
    sites = ["example.com", "example.org", "example.net"]
    tasks = [asyncio.create_task(fetch_data(site)) for site in sites]

    timeout = 10

    try:
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=timeout)
    except asyncio.TimeoutError:
        print(
            f"\nTimeout reached after {timeout} seconds. Cancelling tasks...\n")
        for task in tasks:
            task.cancel()

        # Wait for all tasks to handle cancellation
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for site, result in zip(sites, results):
            if isinstance(result, asyncio.CancelledError):
                print(f"[{site}] Cancelled successfully.")
            elif isinstance(result, Exception):
                print(f"[{site}] Failed with exception: {result}")
            else:
                print(f"[{site}] Finished normally (unexpected).")

    print("\nAll tasks shut down cleanly.")

if __name__ == "__main__":
    asyncio.run(main())
