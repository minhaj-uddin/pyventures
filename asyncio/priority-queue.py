import asyncio


async def worker(name, queue):
    while True:
        priority, task = await queue.get()
        print(f"[{name}] Processing {task} (priority {priority})")
        await asyncio.sleep(1)
        queue.task_done()


async def main():
    queue = asyncio.PriorityQueue()

    # Enqueue tasks (priority, data)
    tasks = [
        (2, "normal-task-1"),
        (1, "urgent-task"),
        (3, "low-task"),
        (2, "normal-task-2"),
    ]

    for item in tasks:
        await queue.put(item)

    # Start worker task
    worker_task = asyncio.create_task(worker("Worker-1", queue))

    await queue.join()
    worker_task.cancel()

asyncio.run(main())
