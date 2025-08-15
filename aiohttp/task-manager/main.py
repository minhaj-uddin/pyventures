from aiohttp import web
from routes import routes
from middlewares import error_middleware, logging_middleware


def create_app():
    app = web.Application(middlewares=[logging_middleware, error_middleware])
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=8080)


# Create a task:
# curl -X POST http://127.0.0.1:8080/tasks \
# -H "Content-Type: application/json" \
# -d '{"title": "Buy milk", "description": "Remember to get fresh milk"}'

# Get all tasks:
# curl -X GET http://127.0.0.1:8080/tasks

# Get a specific task:
# curl -X GET http://127.0.0.1:8080/tasks/1

# Update a task:
# curl -X PUT http://127.0.0.1:8080/tasks/1 \
# -H "Content-Type: application/json" \
# -d '{"title": "Buy almond milk", "description": "Get fresh almond milk"}'

# Delete a task:
# curl -X DELETE http://127.0.0.1:8080/tasks/1

# List tasks with pagination:
# curl -X GET "http://127.0.0.1:8080/tasks?page=1&limit=10"

# List tasks with filtering:
# curl -X GET "http://127.0.0.1:8080/tasks?status=completed"

# List tasks with sorting:
# curl -X GET "http://127.0.0.1:8080/tasks?sort=created_at&order=desc"

# List tasks with search:
# curl -X GET "http://127.0.0.1:8080/tasks?search=milk"
