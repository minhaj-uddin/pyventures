import hashlib
from multiprocessing import Process, Queue


def compute_hash(file_path, result_queue):
    with open(file_path, "rb") as f:
        file_data = f.read()
        file_hash = hashlib.sha256(file_data).hexdigest()

    result_queue.put((file_path, file_hash))


def main():
    files_to_hash = ["file1.txt", "file2.txt", "file3.txt"]

    for file in files_to_hash:
        with open(file, "w") as temp:
            temp.write(f"This is some data in {file}")

    result_queue = Queue()
    processes = []

    for file_path in files_to_hash:
        p = Process(target=compute_hash, args=(file_path, result_queue))
        p.start()
        processes.append(p)

    # Wait for all hashing processes to complete
    for p in processes:
        p.join()

    print("✅ File Hashes:")
    while not result_queue.empty():
        filename, file_hash = result_queue.get()
        print(f"{filename}: {file_hash}")


if __name__ == "__main__":
    main()
