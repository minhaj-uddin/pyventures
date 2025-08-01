import asyncio


async def tcp_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 65432)

    message = "Hello async server!"
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(1024)
    print(f"Received: {data.decode()}")

    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_client())
