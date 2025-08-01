import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Server disconnected.")
                break
            print(f"Received: {data.decode().strip()}")
        except ConnectionAbortedError:
            break
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


def main():
    try:
        # Create a socket and connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")

            # Start thread to listen for messages from the server
            recv_thread = threading.Thread(target=receive_messages, args=(s,))
            recv_thread.daemon = True
            recv_thread.start()

            while True:
                message = input("Enter message (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Closing connection.")
                    break
                s.sendall(message.encode())

    except ConnectionRefusedError:
        print(f"Could not connect to server at {HOST}:{PORT}. Is it running?")
    except KeyboardInterrupt:
        print("\nClient shutting down.")
        sys.exit(0)


if __name__ == "__main__":
    main()
