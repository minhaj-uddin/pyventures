import threading
from queue import Queue

from spider import Spider
from domain import get_domain_name
from file_manager import file_to_set

PROJECT_NAME = 'pyventure'
HOMEPAGE = 'https://webscraper.io/test-sites/e-commerce/static'

DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = f'{PROJECT_NAME}/queue.txt'
CRAWLED_FILE = f'{PROJECT_NAME}/crawled.txt'
NUMBER_OF_THREADS = 8

queue = Queue()
spider = Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work, daemon=True)
        t.start()


def work():
    while True:
        url = queue.get()
        spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if queued_links:
        print(f'{len(queued_links)} links in the queue')
        create_jobs()


if __name__ == '__main__':
    create_workers()
    crawl()
