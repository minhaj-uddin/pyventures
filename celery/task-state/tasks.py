import time
from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('task_state',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

logger = get_task_logger(__name__)


@app.task(bind=True)
def long_running_task(self, total_steps: int):
    for step in range(total_steps):
        time.sleep(0.1)

        # Update progress
        current_progress = (step + 1) / total_steps * 100
        self.update_state(state='PROGRESS',
                          meta={'current': step + 1,
                                'total': total_steps, 'progress': current_progress})

        logger.info(f"Progress: {current_progress:.2f}%")

    return {'status': 'Task Completed!', 'total': total_steps, 'completed': total_steps}
