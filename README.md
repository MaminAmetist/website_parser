Website Parser
Назначение

Website Parser — это Python-парсер сайтов одного домена, который обходит страницы, начиная со стартового URL, и извлекает контактные данные:

email-адреса

телефонные номера

Результат возвращается в виде структурированного объекта.

Проект подходит для:

сбора контактных данных компаний

анализа сайтов

подготовки данных для CRM / лидогенерации

автоматизации ручного поиска контактов

Парсер реализует обход сайта (crawler) с контролем посещённых страниц и ограничением одним доменом — это стандартный подход при построении web-crawler’ов, чтобы избежать бесконечного перехода между сайтами.

Преимущества

Обход всех страниц домена

Поддержка относительных и абсолютных ссылок

Поиск контактов не только на главной странице

Устойчивость к ошибкам сети и HTML

Поддержка IDN-доменов (кириллица и др.)

Нормализация найденных контактов

Расширяемая архитектура

Входные данные
start_url: str


Абсолютный URL сайта, с которого начинается обход.

Выходные данные
{
  "url": "https://example.com",
  "emails": ["info@example.com"],
  "phones": ["+1234567890"]
}


Если контакты не найдены — возвращаются пустые списки.

Установка
git clone https://github.com/MaminAmetist/website_parser.git
cd website_parser
pip install -r requirements.txt

Запуск
python main.py


Или из кода:

from parser import WebsiteParser

parser = WebsiteParser(start_url="https://example.com")
result = parser.parse()

print(result)

Архитектура (кратко)

Основные компоненты:

Crawler / Parser — обход страниц сайта

Link extractor — извлечение ссылок

Contact extractor — поиск email и телефонов

Normalizer — очистка и валидация контактов

Ограничения

Работает только в пределах одного домена

Не обходит JS-рендеринг (если нет headless browser)

Качество извлечения зависит от HTML сайта

Возможные улучшения

Асинхронный обход страниц

Поддержка JavaScript (Playwright / Selenium)

Сохранение результатов в БД

CLI-интерфейс

Настройка глубины обхода

```bash

ParseResult(url='https://xn----8sbpalkejf7aiscg.xn--p1ai/', emails=['export.evgeny@yandex.ru', 'info@ит-маркетплейс.рф'], phones=['+78314140552'])

```


```bash
ParseResult(url='https://habr.com/', emails=['AlBorshchov@korusconsulting.ru', 'EOrlova@korusconsulting.ru', 'claude-code-reflection-skills@claude-code-reflection-skills', 'corp@habr.team', 'userHome@mail.ru'], phones=['+78123052197'])

```