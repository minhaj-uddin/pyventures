import asyncio
import logging


HOST = '127.0.0.1'
PORT = 65432

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    logging.info(f'Connected by {addr}')

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode().strip()
            logging.info(f"Received from {addr}: {message}")
            writer.write(data)
            await writer.drain()
    except (asyncio.IncompleteReadError, ConnectionResetError) as e:
        logging.warning(f'Error with {addr}: {e}')
    finally:
        writer.close()
        await writer.wait_closed()
        logging.info(f'Disconnected {addr}')


async def shutdown(server):
    logging.info("Shutting down server...")
    server.close()
    await server.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    logging.info(f'Server listening on {addr}')

    try:
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Received exit signal (KeyboardInterrupt)")
        await shutdown(server)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
