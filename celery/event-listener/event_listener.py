import logging
from celery import Celery
from celery.events import EventReceiver
from kombu import Connection
from typing import Callable

from utils import format_event

logger = logging.getLogger(__name__)


class CeleryEventListener:
    def __init__(self, broker_url: str, app: Celery | None = None) -> None:
        self.broker_url = broker_url
        self.app = app or Celery(broker=broker_url)

    def _handle_event(self, event: dict) -> None:
        event_type = event.get("type")
        formatted = format_event(event)
        logger.info(f"[{event_type}] {formatted}")

    def start(self, handler: Callable[[dict], None] | None = None) -> None:
        handler = handler or self._handle_event
        with Connection(self.broker_url) as conn:
            recv = EventReceiver(
                conn,
                handlers={"*": handler},
                app=self.app,
            )
            logger.info("Starting to capture Celery task events...")
            recv.capture(limit=None, timeout=None, wakeup=True)
