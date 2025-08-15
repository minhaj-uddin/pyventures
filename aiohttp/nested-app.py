from aiohttp import web


# Admin-only middleware
@web.middleware
async def admin_logging_middleware(request, handler):
    print(f"[ADMIN] {request.method} {request.path}")
    return await handler(request)


# Handler in main app
async def public_home(request):
    return web.Response(text="Welcome to the main site!")


# Handler in admin sub-app
async def admin_dashboard(request):
    return web.Response(text="Welcome to the admin dashboard!")

# Create the admin sub-app
admin_app = web.Application(middlewares=[admin_logging_middleware])
admin_app.router.add_get('/', admin_dashboard)
admin_app.router.add_get(
    '/settings', lambda _: web.Response(text="Settings page"))

# Create the main app
main_app = web.Application()
main_app.router.add_get('/', public_home)

# Mount the admin app under /admin
main_app.add_subapp('/admin', admin_app)

# Run the app
web.run_app(main_app, host="127.0.0.1", port=8080)
