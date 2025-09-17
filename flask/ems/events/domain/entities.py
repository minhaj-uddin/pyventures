from .exceptions import EventFull, UserAlreadyRegistered


class Event:
    def __init__(self, event_id, name, capacity):
        self.id = event_id
        self.name = name
        self.capacity = capacity
        self.attendees = []

    def register_user(self, user_id):
        if user_id in self.attendees:
            raise UserAlreadyRegistered("User already registered")
        if len(self.attendees) >= self.capacity:
            raise EventFull("Event has reached full capacity")
        self.attendees.append(user_id)
