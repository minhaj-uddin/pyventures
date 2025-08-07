import asyncio


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Client connected: {addr}")

    data = await reader.read(1024)
    message = data.decode()
    print(f"Received: {message}")

    response = f"Echo: {message}"
    writer.write(response.encode())
    await writer.drain()

    print("Closing connection.")
    writer.close()
    await writer.wait_closed()


async def main():
    try:
        server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
        print("Server running on 127.0.0.1:8888")
        async with server:
            await server.serve_forever()
    except asyncio.CancelledError:
        print("Server cancelled.")

if __name__ == "__main__":
    asyncio.run(main())
