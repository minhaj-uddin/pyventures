import socket
import threading
import logging
import signal
import sys

HOST = '127.0.0.1'
PORT = 65432

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def signal_handler(sig, frame):
    logging.info('Shutting down server...')
    server_socket.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def handle_client(conn, addr):
    logging.info(f'Connected by {addr}')
    with conn:
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                logging.info(f"Received from {addr}: {data.decode().strip()}")
                conn.sendall(data)
        except ConnectionResetError:
            logging.warning(f'Connection reset by {addr}')
    logging.info(f'Disconnected {addr}')


# Create and configure socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

logging.info(f'Server listening on {HOST}:{PORT}')

# Main loop: Accept clients
try:
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()
except Exception as e:
    logging.error(f'Server error: {e}')
finally:
    server_socket.close()
