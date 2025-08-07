from urllib.request import urlopen
from file_manager import create_project_dir, create_data_files, file_to_set, set_to_file
from domain import get_domain_name
from link_finder import LinkFinder


class Spider:
    def __init__(self, project_name: str, base_url: str, domain_name: str):
        self.project_name = project_name
        self.base_url = base_url
        self.domain_name = domain_name
        self.queue_file = f'{project_name}/queue.txt'
        self.crawled_file = f'{project_name}/crawled.txt'
        self.queue = set()
        self.crawled = set()
        self.boot()
        self.crawl_page('First spider', self.base_url)

    def boot(self):
        create_project_dir(self.project_name)
        create_data_files(self.project_name, self.base_url)
        self.queue = file_to_set(self.queue_file)
        self.crawled = file_to_set(self.crawled_file)

    def crawl_page(self, thread_name: str, page_url: str):
        if page_url not in self.crawled:
            print(f'{thread_name} crawling {page_url}')
            print(f'Queue: {len(self.queue)} | Crawled: {len(self.crawled)}')
            links = self.gather_links(page_url)
            self.add_links_to_queue(links)
            self.queue.discard(page_url)
            self.crawled.add(page_url)
            self.update_files()

    def gather_links(self, page_url: str) -> set:
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html = response.read().decode('utf-8')
                finder = LinkFinder(self.base_url, page_url)
                finder.feed(html)
                return finder.page_links()
        except Exception as e:
            print(f'Error: {e}')
        return set()

    def add_links_to_queue(self, links: set):
        for url in links:
            if url in self.queue or url in self.crawled:
                continue
            if self.domain_name != get_domain_name(url):
                continue
            self.queue.add(url)

    def update_files(self):
        set_to_file(self.queue, self.queue_file)
        set_to_file(self.crawled, self.crawled_file)
