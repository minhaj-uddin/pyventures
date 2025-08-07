import os
import sys
import signal
import asyncio


async def main():
    print("Event loop running. Press Ctrl+C to exit.")
    print(f"PID {os.getpid()}: Send SIGINT or SIGTERM to stop.")

    stop_event = asyncio.Event()

    def shutdown():
        print("Shutdown signal received.")
        stop_event.set()

    loop = asyncio.get_running_loop()

    try:
        # UNIX systems (Linux/macOS)
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, shutdown)
    except NotImplementedError:
        # Windows fallback
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, lambda s, f: shutdown())

    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        print("Main coroutine cancelled.")
    finally:
        print("Shutting down gracefully...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt received.")
        sys.exit(0)
