from typing import Set

from bs4 import BeautifulSoup

from config import ParserConfig, ParseResult
from contacts import ContactExtractor
from parser import DomainParser
from url_validator import UrlValidator

from html_loader import UniversalHtmlLoader, BrowserHtmlLoader


class StartParser:
    """Запускает парсинг сайта."""

    def __init__(
        self,
        start_url: str,
        config: ParserConfig | None = None,
    ) -> None:
        UrlValidator.validate(start_url)

        self.start_url = start_url
        self.config = config or ParserConfig()

        self.crawler = DomainParser(start_url, self.config)

        # loaders
        self.browser_loader = BrowserHtmlLoader()
        self.http_loader = UniversalHtmlLoader(self.browser_loader)


    def _load_html_with_fallback(self, url: str) -> str:
        """
        Загружает HTML:
        1) HTTP
        2) Browser fallback
        """
        html = self.http_loader.load(url)
        if not html:
            html = self.browser_loader.load(url)

        if not html or len(html) < 1500:
            html = self.browser_loader.load(url)

        return html

    def _extract_contacts(self, html: str) -> tuple[Set[str], Set[str]]:
        """Извлекает контакты из HTML."""
        soup = BeautifulSoup(html, "html.parser")

        emails = ContactExtractor.extract_emails(soup)
        phones = ContactExtractor.extract_phones(soup)

        return emails, phones

    def parse(self) -> ParseResult:
        """
        Запускает парсинг сайта.
        """
        emails: Set[str] = set()
        phones: Set[str] = set()

        for url in self.crawler.crawl():
            html = self._load_html_with_fallback(url)

            page_emails, page_phones = self._extract_contacts(html)

            # если email нет — пробуем browser (динамика)
            if not page_emails:
                browser_html = self.browser_loader.load(url)
                page_emails, page_phones = self._extract_contacts(browser_html)

            emails |= page_emails
            phones |= page_phones

        return ParseResult(
            url=self.start_url,
            emails=sorted(emails),
            phones=sorted(phones),
        )


if __name__ == "__main__":
    parser = StartParser("https://habr.com/")
    result = parser.parse()

    print(result)
