from celery import Celery
from celery.events.state import State
from celery.events.receiver import EventReceiver


def event_monitor(app):
    state = State()

    def receive_failed_tasks(event):
        state.event(event)
        task = state.tasks.get(event['uuid'])

        if task:
            print(f"TASK FAILED: {task.name}[{task.uuid}] — {task.exception}")
        else:
            print(f"TASK FAILED (no state info): {event['uuid']}")

    with app.connection() as conn:
        recv = EventReceiver(conn, handlers={
            'task-failed': receive_failed_tasks,
            '*': state.event,
        })
        print("Started monitoring failed tasks...")
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == "__main__":
    app = Celery("events", broker='redis://localhost:6379/0')
    event_monitor(app)
