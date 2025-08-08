import os
from abc import ABC, abstractmethod
from multiprocessing import Process, Queue, set_start_method


def producer_runner(produce_func, task_queue, num_workers):
    produce_func(task_queue)
    for _ in range(num_workers):
        task_queue.put(None)


def worker_runner(process_func, task_queue, result_queue):
    while True:
        task = task_queue.get()
        if task is None:
            break
        result = process_func(task)
        if result is not None:
            result_queue.put(result)


class JobQueue(ABC):
    def __init__(self, num_workers=None):
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.num_workers = num_workers or os.cpu_count()
        self.workers = []

    def start(self):
        print("🚀 Starting job queue ...")

        # Start producer
        producer = Process(
            target=producer_runner,
            args=(self.produce_tasks, self.task_queue, self.num_workers)
        )
        producer.start()

        # Start workers
        for _ in range(self.num_workers):
            p = Process(
                target=worker_runner,
                args=(self.process_task, self.task_queue, self.result_queue)
            )
            p.start()
            self.workers.append(p)

        # Wait for producer
        producer.join()

        # Wait for workers
        for worker in self.workers:
            worker.join()

        print("✅ All workers finished. Collecting results...")
        while not self.result_queue.empty():
            self.handle_result(self.result_queue.get())

    # --- Abstract methods ---
    @staticmethod
    @abstractmethod
    def produce_tasks(task_queue):
        pass

    @staticmethod
    @abstractmethod
    def process_task(task):
        pass

    @staticmethod
    @abstractmethod
    def handle_result(result):
        pass


class WordCountJob(JobQueue):
    def __init__(self, input_dir, num_workers=None):
        super().__init__(num_workers)
        self.input_dir = input_dir

    @staticmethod
    def produce_tasks(task_queue):
        for filename in os.listdir("texts"):
            if filename.endswith(".txt"):
                full_path = os.path.join("texts", filename)
                task_queue.put(full_path)

    @staticmethod
    def process_task(file_path):
        with open(file_path, "r") as f:
            text = f.read()
        word_count = len(text.split())
        return (os.path.basename(file_path), word_count)

    @staticmethod
    def handle_result(result):
        filename, count = result
        print(f"{filename}: {count} words")


def prepare_demo_files():
    os.makedirs("texts", exist_ok=True)
    for i in range(5):
        with open(f"texts/file{i + 1}.txt", "w") as f:
            f.write("This is a line.\n" * (i + 1))


if __name__ == "__main__":
    try:
        set_start_method("spawn")
    except RuntimeError:
        print("Spawn method already set, continuing...")
        pass

    prepare_demo_files()
    job = WordCountJob(input_dir="texts")
    job.start()
