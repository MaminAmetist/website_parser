import re
from typing import Set
from bs4 import BeautifulSoup
import idna


class ContactExtractor:
    """Извлечение контактных данных из HTML."""

    EMAIL_REGEX = re.compile(
        r"[a-zA-Z0-9._%+-]+@[^\s\"'>]+",
        re.UNICODE,
    )

    PHONE_REGEX = re.compile(
        r"(?:\+7|8)\s*[\(\d][\d\s\-\(\)]{8,}\d"
    )

    @classmethod
    def extract_emails(cls, soup: BeautifulSoup) -> Set[str]:
        """
        Извлекает email из текста и mailto-ссылок.
        """
        emails: Set[str] = set()

        # 1. Текст
        text = soup.get_text(separator=" ")
        emails |= cls._extract_from_text(text)

        # 2. mailto:
        for tag in soup.find_all("a", href=True):
            href: str = tag["href"]
            if href.lower().startswith("mailto:"):
                email = href[7:].split("?")[0]
                emails |= cls._normalize_email(email)

        return emails

    @classmethod
    def extract_phones(cls, soup: BeautifulSoup) -> Set[str]:
        """Извлекает и нормализует телефоны."""
        phones: Set[str] = set()
        text = soup.get_text(separator=" ")

        for raw in cls.PHONE_REGEX.findall(text):
            digits = re.sub(r"\D", "", raw)

            if len(digits) != 11:
                continue

            if digits.startswith("8"):
                digits = "7" + digits[1:]

            phones.add(f"+{digits}")

        return phones

    @classmethod
    def _extract_from_text(cls, text: str) -> Set[str]:
        found: Set[str] = set()
        for raw in cls.EMAIL_REGEX.findall(text):
            found |= cls._normalize_email(raw)
        return found

    @staticmethod
    def _normalize_email(raw: str) -> Set[str]:
        try:
            local, domain = raw.split("@", 1)
            idna.encode(domain)  # IDN validation
            return {f"{local}@{domain}"}
        except (ValueError, idna.IDNAError, UnicodeError):
            return set()
