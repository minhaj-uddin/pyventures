import asyncio


async def tcp_client(host='127.0.0.1', port=8888):
    try:
        print(f"Connecting to {host}:{port}...")
        reader, writer = await asyncio.open_connection(host, port)
        print("Connected.")

        message = "Hello, server!"
        print(f"Sending: {message}")
        writer.write(message.encode())
        await writer.drain()

        response = await reader.read(1024)
        print(f"Received: {response.decode()}")

        print("Closing the connection.")
        writer.close()
        await writer.wait_closed()

    except ConnectionRefusedError:
        print(f"Could not connect to {host}:{port} — is the server running?")


async def main():
    await tcp_client()

if __name__ == "__main__":
    asyncio.run(main())
