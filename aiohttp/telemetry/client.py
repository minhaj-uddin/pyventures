import aiohttp
import asyncio
import random
import time

# Define the URL of your running server
SERVER_URL = 'http://localhost:8080/telemetry'


def generate_telemetry():
    return {
        "sensor_id": f"sensor_{random.randint(1, 10)}",
        "timestamp": int(time.time()),
        "value": round(random.uniform(0, 100), 2)
    }


async def send_telemetry(session):
    while True:
        # Generate random telemetry data
        telemetry_data = generate_telemetry()
        # Send the telemetry data as JSON to the server
        async with session.post(SERVER_URL, json=telemetry_data) as response:
            # Log the server response
            if response.status == 200:
                print(f"Telemetry sent: {telemetry_data}")
            else:
                print(f"Error sending telemetry: {response.status}, {await response.text()}")
        # Wait for a short while
        await asyncio.sleep(1)


# Main entry point
async def main():
    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        # Start sending telemetry data
        await send_telemetry(session)

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
