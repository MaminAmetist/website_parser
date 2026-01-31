import time
from typing import Iterable, Set, List
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests import Response
from requests.exceptions import RequestException

from config import ParserConfig
from html_loader import UniversalHtmlLoader


class DomainParser:
    """Обходит страницы сайта в пределах одного домена."""

    def __init__(self, start_url: str, config: ParserConfig, loader: UniversalHtmlLoader=None) -> None:
        self.start_url = start_url
        self.config = config
        self.domain = urlparse(start_url).netloc
        self.visited: Set[str] = set()
        self.loader = loader

    def crawl(self) -> Iterable[str]:
        """
        Итератор HTML-страниц сайта.

        Yields:
            HTML-код страницы
        """
        queue: List[str] = [self.start_url]

        while queue and len(self.visited) < self.config.max_pages:
            url = queue.pop(0)

            if url in self.visited:
                continue

            self.visited.add(url)

            try:
                response = self._fetch(url)
            except RequestException:
                continue

            yield response.text

            links = self._extract_links(response, base_url=url)
            queue.extend(link for link in links if link not in self.visited)

            time.sleep(self.config.sleep_between_requests)

    def _fetch_html(self, url: str) -> str:
        return self.loader.load(url)


    def _fetch(self, url: str) -> Response:
        """Загружает страницу."""
        print(111111111111111111111111)
        headers = {"User-Agent": self.config.user_agent}
        response = requests.get(url, timeout=self.config.timeout, headers=headers)
        response.raise_for_status()
        return response

    def _extract_links(self, response: Response, base_url: str) -> Set[str]:
        soup = BeautifulSoup(response.text, "html.parser")
        links: Set[str] = set()

        for tag in soup.find_all("a", href=True):
            absolute = urljoin(base_url, tag["href"])
            parsed = urlparse(absolute)

            if parsed.netloc == self.domain:
                links.add(parsed.geturl())

        return links
