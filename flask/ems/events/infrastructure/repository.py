from domain.entities import Event


class InMemoryEventRepository:
    def __init__(self):
        self._events = {
            1: Event(1, "FlaskConf", 120),
            2: Event(2, "PyHackathon", 20)
        }

    def get_event_by_id(self, event_id):
        return self._events.get(event_id)

    def save(self, event: Event):
        self._events[event.id] = event
