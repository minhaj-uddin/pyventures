import os
import random
import asyncio
from aiohttp import web, ClientConnectionError


async def stock_price_feed(request):
    response = web.StreamResponse(
        status=200,
        reason='OK',
        headers={
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        },
    )
    await response.prepare(request)

    symbols = ['AAPL', 'GOOG', 'TSLA', 'AMZN', 'MSFT']

    try:
        while True:
            symbol = random.choice(symbols)
            price = round(random.uniform(100, 1500), 2)
            data = f"{symbol}: ${price}"
            try:
                await response.write(f"data: {data}\n".encode('utf-8'))
            except (ConnectionResetError, asyncio.CancelledError, ClientConnectionError):
                print("Client disconnected.")
                break
            await asyncio.sleep(1)
    finally:
        try:
            await response.write_eof()
        except ConnectionResetError:
            print("Client already disconnected.")
            pass

    return response

# --- Set up App ---
app = web.Application()

# Serve static files from the same directory
static_path = os.path.dirname(__file__)
print(f"Serving static files from: {static_path}")
app.router.add_static('/', static_path, show_index=True)

# SSE endpoint
app.router.add_get('/sse', stock_price_feed)

if __name__ == '__main__':
    web.run_app(app, port=8080)
