import time
from tqdm import tqdm
from tasks import long_running_task


def display_progress(task_id: str, total_steps: int):
    # Initialize tqdm progress bar
    progress_bar = tqdm(total=total_steps,
                        desc="Task Progress", unit="step", ncols=100)

    while True:
        result = long_running_task.AsyncResult(task_id)

        # Check if the task has finished
        if result.state == 'SUCCESS':
            print("Task completed successfully!")
            break
        elif result.state == 'PROGRESS':
            # Get progress information from the task result
            progress = result.info.get('progress', 0)

            # Update the tqdm progress bar
            progress_bar.n = result.info.get('current', 0)
            progress_bar.last_print_n = progress_bar.n
            progress_bar.update(0)

        else:
            print("Waiting for task to start...")
            time.sleep(1)


def start_task():
    total_steps = 100
    task = long_running_task.apply_async((total_steps,))
    print(f"Task started with ID: {task.id}")

    # Display progress in the CLI
    task.get(on_message=display_progress(
        task.id, total_steps), propagate=False)


if __name__ == '__main__':
    start_task()
