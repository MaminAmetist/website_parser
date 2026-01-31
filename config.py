from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ParserConfig:
    """Конфигурация парсера."""

    timeout: int = 10
    max_pages: int = 100
    sleep_between_requests: float = 0.3
    user_agent: str = "SiteParserBot/1.0"


@dataclass
class ParseResult:
    """Результат работы парсера."""

    url: str
    emails: List[str]
    phones: List[str]
