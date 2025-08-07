import asyncio


async def background_worker(trigger_event: asyncio.Event):
    print("[Worker] Waiting for trigger...")
    await trigger_event.wait()  # Wait for the event to be set
    print("[Worker] Trigger received! Starting processing...")
    await asyncio.sleep(3)  # Simulate work
    print("[Worker] Done processing.")


async def simulate_trigger(event: asyncio.Event):
    await asyncio.sleep(5)  # Simulate a delay
    print("[Trigger] Setting the event.")
    event.set()  # Unblocks the waiting worker


async def main():
    event = asyncio.Event()
    worker = asyncio.create_task(background_worker(event))
    trigger = asyncio.create_task(simulate_trigger(event))

    await asyncio.gather(worker, trigger)

if __name__ == "__main__":
    asyncio.run(main())
