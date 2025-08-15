import asyncio
from aiohttp import ClientSession, ClientTimeout


async def fetch_with_retry(url, headers, session):
    for attempt in range(3):
        try:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                return await resp.json()
        except asyncio.TimeoutError:
            if attempt == 2:
                return {"error": "timeout", "url": url}
            await asyncio.sleep(0.2)


async def aggregate_patient_data(pid):
    headers = {"X-Forwarded-For": "api-proxy"}
    timeout = ClientTimeout(total=5)
    async with ClientSession(timeout=timeout) as session:
        base = f"https://ehr.example.com/patient/{pid}"
        resp1 = await fetch_with_retry(base + "/demographics", headers, session)
        resp2 = await fetch_with_retry(base + "/conditions", headers, session)
        return {"demographics": resp1, "conditions": resp2}
