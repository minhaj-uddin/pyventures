import re
from aiohttp import web


def validate_patient_id(request):
    pid = request.query.get("patient_id")
    if not pid or not re.match(r'^[A-Za-z0-9\-]+$', pid):
        raise web.HTTPBadRequest(text="Invalid or missing patient_id")
    return pid
