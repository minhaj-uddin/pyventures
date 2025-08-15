import store as db
from aiohttp import web
from utils import validate_task_data

routes = web.RouteTableDef()


@routes.get('/tasks')
async def list_tasks(request):
    page = int(request.query.get('page', 1))
    limit = int(request.query.get('limit', 10))
    status = request.query.get('status')
    sort_by = request.query.get('sort', 'created_at')
    order = request.query.get('order', 'asc')
    search = request.query.get('search')

    tasks = await db.get_tasks(page=page, limit=limit, status=status,
                               sort_by=sort_by, order=order, search=search)

    return web.json_response(tasks)


@routes.post('/tasks')
async def create(request):
    data = await request.json()
    data = validate_task_data(data)
    task = await db.create_task(data['title'], data['description'])
    return web.json_response(task, status=201)


@routes.get('/tasks/{task_id}')
async def get(request):
    task_id = request.match_info['task_id']
    task = await db.get_task(task_id)
    if not task:
        raise web.HTTPNotFound(reason="Task not found")
    return web.json_response(task)


@routes.put('/tasks/{task_id}')
async def update(request):
    task_id = request.match_info['task_id']
    data = await request.json()
    task = await db.update_task(task_id, data)
    if not task:
        raise web.HTTPNotFound(reason="Task not found")
    return web.json_response(task)


@routes.delete('/tasks/{task_id}')
async def delete(request):
    task_id = request.match_info['task_id']
    task = await db.delete_task(task_id)
    if not task:
        raise web.HTTPNotFound(reason="Task not found")
    return web.json_response({'status': 'deleted'})
