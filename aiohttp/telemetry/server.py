import asyncio
import logging
from aiohttp import web
from pydantic import BaseModel, ValidationError

# Set up logging
logging.basicConfig(level=logging.INFO)


# 1. Pydantic Model for Telemetry Data
class TelemetryData(BaseModel):
    sensor_id: str
    timestamp: int
    value: float


# 2. In-memory Queue for Telemetry Data
telemetry_queue = asyncio.Queue()


# 3. Process telemetry data
async def process_telemetry_data():
    while True:
        telemetry = await telemetry_queue.get()
        if telemetry is None:
            break  # Graceful shutdown signal
        logging.info(f"Processing telemetry data: {telemetry}")
        # Add your data processing logic here
        await asyncio.sleep(10)


# 4. REST API Endpoint to receive telemetry data
async def receive_telemetry(request):
    try:
        data = await request.json()
        telemetry = TelemetryData(**data)
        logging.info(f"Received telemetry data: {telemetry}")

        # Add the validated telemetry data to the queue
        await telemetry_queue.put(telemetry)
        return web.Response(status=200, text="Telemetry data received")

    except ValidationError as e:
        return web.Response(status=400, text=f"Invalid data: {e}")

    except Exception as e:
        logging.error(f"Error receiving telemetry data: {e}")
        return web.Response(status=500, text="Internal Server Error")


# 5. Graceful Shutdown
async def shutdown(app):
    logging.info("Shutting down gracefully...")
    # Signal to stop the processing loop
    await telemetry_queue.put(None)


# 6. Create and run the aiohttp server
async def init():
    app = web.Application()
    app.add_routes([web.post('/telemetry', receive_telemetry)])

    # Start the background task to process telemetry data
    app['background_task'] = asyncio.create_task(process_telemetry_data())

    # Handle graceful shutdown
    app.on_shutdown.append(shutdown)

    return app

# Main entry point
if __name__ == '__main__':
    try:
        web.run_app(init(), host='127.0.0.1', port=8080)
    except KeyboardInterrupt:
        logging.info("Server interrupted, shutting down...")
