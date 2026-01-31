# Website Parser

## Назначение

Website Parser это Python-парсер сайтов одного домена, который обходит страницы, начиная со стартового URL, и
извлекает контактные данные: email-адреса и телефонные номера.
Результат возвращается в виде структурированного объекта.
Парсер реализует обход сайта с контролем посещённых страниц и ограничением одним доменом — это стандартный подход при
построении web-crawler’ов, чтобы избежать бесконечного перехода между сайтами.

## Преимущества

Обход всех страниц домена

Поддержка относительных и абсолютных ссылок

Поиск контактов не только на главной странице

Устойчивость к ошибкам сети и HTML

Поддержка IDN-доменов (кириллица и др.)

Нормализация найденных контактов

Расширяемая архитектура

## Входные данные

Абсолютный URL сайта, с которого начинается обход:

start_url: str

## Выходные данные

```bash

ParseResult(url='https://xn----8sbpalkejf7aiscg.xn--p1ai/', emails=['export.evgeny@yandex.ru', 'info@ит-маркетплейс.рф'], phones=['+78314140552'])

```

```bash
ParseResult(url='https://habr.com/', emails=['AlBorshchov@korusconsulting.ru', 'EOrlova@korusconsulting.ru', 'claude-code-reflection-skills@claude-code-reflection-skills', 'corp@habr.team', 'userHome@mail.ru'], phones=['+78123052197'])

```

Если контакты не найдены — возвращаются пустые списки.

## Установка

```bash
git clone https://github.com/MaminAmetist/website_parser.git
cd website_parser
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```
