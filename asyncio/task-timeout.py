import random
import asyncio


async def fetch_data(site: str):
    while True:
        print(f"[{site}] Fetching data...")
        await asyncio.sleep(random.uniform(1, 3))
        print(f"[{site}] Done.")


async def main():
    sites = ["example.com", "example.org", "example.net"]
    tasks = [fetch_data(site) for site in sites]

    timeout = 5

    try:
        # Run all scraper tasks for `timeout` seconds
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=timeout)
    except asyncio.TimeoutError:
        print(f"\nTimeout reached after {timeout} seconds. Stopping.")

if __name__ == "__main__":
    asyncio.run(main())
