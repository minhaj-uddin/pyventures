import time
import atexit
import requests
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

session: requests.Session


def main():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 10
    start_time = time.perf_counter()
    download_all_sites(sites)
    duration = time.perf_counter() - start_time
    print(f"Downloaded {len(sites)} sites in {duration:.2f} seconds")


def download_all_sites(sites):
    with ProcessPoolExecutor(initializer=init_process) as executor:
        executor.map(download_site, sites)


def download_site(url):
    with session.get(url) as response:
        name = multiprocessing.current_process().name
        print(f"{name}:Read {len(response.content)} bytes from {url}")


def init_process():
    global session
    session = requests.Session()
    atexit.register(session.close)


if __name__ == "__main__":
    main()
