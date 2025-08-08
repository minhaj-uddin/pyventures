import os
from multiprocessing import Process, Queue


def producer(task_queue, input_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            task_queue.put(os.path.join(input_dir, filename))

    for _ in range(os.cpu_count()):
        task_queue.put(None)


def consumer(task_queue, result_queue):
    while True:
        file_path = task_queue.get()
        if file_path is None:
            break

        with open(file_path, "r") as f:
            content = f.read()
            word_count = len(content.split())
            result = (os.path.basename(file_path), word_count)
            result_queue.put(result)


def main():
    input_dir = "texts"
    os.makedirs(input_dir, exist_ok=True)

    for i in range(5):
        with open(os.path.join(input_dir, f"file{i}.txt"), "w") as f:
            f.write("This is some sample text.\n" * (i + 1))

    task_queue = Queue()
    result_queue = Queue()

    # Start producer
    producer_process = Process(target=producer, args=(task_queue, input_dir))
    producer_process.start()

    # Start worker consumers
    num_workers = min(4, os.cpu_count())
    workers = []

    for _ in range(num_workers):
        p = Process(target=consumer, args=(task_queue, result_queue))
        p.start()
        workers.append(p)

    # Wait for producer to finish
    producer_process.join()

    # Wait for all workers to finish
    for worker in workers:
        worker.join()

    # Collect results
    print("✅ Word Counts from Each File:")
    while not result_queue.empty():
        filename, count = result_queue.get()
        print(f"{filename}: {count} words")


if __name__ == "__main__":
    main()
