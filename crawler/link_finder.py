from html.parser import HTMLParser
from urllib.parse import urljoin


class LinkFinder(HTMLParser):
    def __init__(self, base_url: str, page_url: str):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attribute, value in attrs:
                if attribute == 'href':
                    url = urljoin(self.base_url, value)
                    self.links.add(url)

    def page_links(self) -> set:
        return self.links
