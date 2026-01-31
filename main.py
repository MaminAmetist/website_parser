from dataclasses import asdict
from typing import Set

from bs4 import BeautifulSoup

from config import ParserConfig, ParseResult
from contacts import ContactExtractor
from parser import DomainParser
from url_validator import UrlValidator


class StartParser:
    """Запускает парсинг сайта."""

    def __init__(self, start_url: str, config: ParserConfig | None = None) -> None:
        UrlValidator.validate(start_url)

        self.start_url = start_url
        self.config = config or ParserConfig()
        self.crawler = DomainParser(start_url, self.config)

    def parse(self) -> ParseResult:
        """
        Запускает парсинг сайта.

        :return: ParseResult
        """
        emails: Set[str] = set()
        phones: Set[str] = set()

        for html in self.crawler.crawl():
            soup = BeautifulSoup(html, "html.parser")

            emails |= ContactExtractor.extract_emails(soup)
            phones |= ContactExtractor.extract_phones(soup)

        return ParseResult(
            url=self.start_url,
            emails=sorted(emails),
            phones=sorted(phones),
        )


if __name__ == '__main__':
    #parser = StartParser("https://xn----8sbpalkejf7aiscg.xn--p1ai/")
    parser = StartParser("https://habr.com/")
    result = parser.parse()

    print(asdict(result))
