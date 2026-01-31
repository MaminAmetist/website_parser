from urllib.parse import urlparse


class UrlValidator:
    """Валидация входного URL."""

    @staticmethod
    def validate(url: str) -> None:
        """
        Проверяет корректность абсолютного URL.

        :raises ValueError: если URL некорректен
        """
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("start_url должен быть абсолютным URL")
