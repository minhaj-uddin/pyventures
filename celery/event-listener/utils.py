from typing import Any


def format_event(event: dict[str, Any]) -> str:
    parts = [f"{key}={value}" for key, value in event.items()]
    return ", ".join(parts)
