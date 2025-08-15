from auth import require_roles
from validation import validate_patient_id
from proxy import aggregate_patient_data
from cache import cache_response
from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/patient')
@require_roles("doctor", "nurse")
@cache_response  # caches per patient_id
async def patient_proxy(request):
    pid = validate_patient_id(request)
    result = await aggregate_patient_data(pid)
    return web.json_response(result)
