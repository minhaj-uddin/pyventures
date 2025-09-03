import logging
from event_listener import CeleryEventListener

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

BROKER_URL = "redis://localhost:6379/0"


def main() -> None:
    listener = CeleryEventListener(broker_url=BROKER_URL)
    listener.start()


if __name__ == "__main__":
    main()
