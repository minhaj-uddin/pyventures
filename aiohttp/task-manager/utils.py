from aiohttp import web


def validate_task_data(data):
    if 'title' not in data or not data['title']:
        raise web.HTTPBadRequest(text="Missing 'title'")
    if 'description' not in data:
        data['description'] = ''
    return data
