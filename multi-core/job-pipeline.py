import os
import string
import logging
from multiprocessing import Process, Queue, set_start_method

logging.basicConfig(
    level=logging.INFO,
    format='%(processName)s - %(message)s'
)


def file_reader(file_list, output_queue):
    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                output_queue.put((os.path.basename(file_path), content))
                logging.info(f"Read {file_path}")
        except Exception as e:
            logging.error(f"Failed to read {file_path}: {e}")
    output_queue.put(None)


def text_cleaner(input_queue, output_queue):
    while True:
        item = input_queue.get()
        if item is None:
            output_queue.put(None)
            break
        filename, text = item
        cleaned = text.lower().translate(str.maketrans('', '', string.punctuation))
        logging.info(f"Cleaned {filename}")
        output_queue.put((filename, cleaned))


def word_counter(input_queue):
    total_words = 0
    while True:
        item = input_queue.get()
        if item is None:
            break
        filename, cleaned_text = item
        word_count = len(cleaned_text.split())
        total_words += word_count
        logging.info(f"{filename}: {word_count} words")
    logging.info(f"TOTAL: {total_words} words")


def prepare_demo_files():
    os.makedirs("texts", exist_ok=True)
    for i in range(5):
        with open(f"texts/file{i + 1}.txt", "w", encoding="utf-8") as f:
            f.write("Hello, world! This is line number.\n" * (i + 1))


def main():
    try:
        set_start_method("spawn")
    except RuntimeError:
        pass

    prepare_demo_files()
    input_files = [os.path.join("texts", f)
                   for f in os.listdir("texts") if f.endswith(".txt")]

    q1 = Queue()  # Between file_reader → text_cleaner
    q2 = Queue()  # Between text_cleaner → word_counter

    p1 = Process(target=file_reader, args=(input_files, q1))
    p2 = Process(target=text_cleaner, args=(q1, q2))
    p3 = Process(target=word_counter, args=(q2,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()


if __name__ == "__main__":
    main()
