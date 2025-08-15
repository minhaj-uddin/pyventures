import uuid
import asyncio
from datetime import datetime

_tasks = {}


def search_tasks(search_term, tasks):
    return [task for task in tasks
            if search_term.lower() in task['title'].lower()
            or search_term.lower() in task['description'].lower()]


async def create_task(title, description):
    task_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    _tasks[task_id] = {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": created_at,
        "updated_at": created_at
    }
    await asyncio.sleep(0)
    return _tasks[task_id]


async def get_task(task_id):
    await asyncio.sleep(0)
    return _tasks.get(task_id)


async def get_tasks(page=1, limit=10, status=None, sort_by="created_at", order="asc", search=None):
    await asyncio.sleep(0)
    tasks = list(_tasks.values())

    # Apply search
    if search:
        tasks = search_tasks(search, tasks)

    # Apply filtering by status
    if status:
        status = status.lower()
        tasks = [task for task in tasks if (status == "completed" and task["completed"])
                 or (status == "incomplete" and not task["completed"])]

    # Sort tasks
    tasks.sort(key=lambda x: x.get(sort_by), reverse=order == "desc")

    # Pagination
    start = (page - 1) * limit
    end = start + limit
    return tasks[start:end]


async def update_task(task_id, data):
    await asyncio.sleep(0)
    if task_id in _tasks:
        _tasks[task_id].update(data)
        _tasks[task_id]["updated_at"] = datetime.now().isoformat()
        return _tasks[task_id]
    return None


async def delete_task(task_id):
    await asyncio.sleep(0)
    return _tasks.pop(task_id, None)
