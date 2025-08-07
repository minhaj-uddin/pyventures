import random
import asyncio


async def fetch_data(site: str):
    print(f"[{site}] Fetching data...")
    await asyncio.sleep(random.uniform(1, 3))
    print(f"[{site}] Done.")


async def main():
    sites = ["example.com", "example.org", "example.net"]
    await asyncio.gather(*(fetch_data(site) for site in sites))

if __name__ == "__main__":
    asyncio.run(main())
