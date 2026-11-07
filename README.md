# YouTrack UI Automation

Проект автоматизации тестирования веб-интерфейса YouTrack с использованием Python, Playwright и pytest.

## Технологический стек

- Python 3.14
- Playwright
- pytest
- pytest-playwright
- pytest-xdist
- python-dotenv
- Ruff
- Docker Compose
- uv

## Реализованные тестовые сценарии

1. Успешная авторизация.
2. Создание задачи.
3. Поиск задачи по ID.
4. Изменение статуса задачи.
5. Добавление комментария к задаче.
6. Проверка негативных сценариев авторизации с использованием параметризации.

## Архитектура

Используется паттерн Page Object Model (POM).

Локаторы и методы взаимодействия со страницами вынесены в отдельные классы. Тестовые сценарии находятся в директории `tests`.

Дополнительно реализованы:

- Data-driven testing через `pytest.mark.parametrize`.
- Fixtures для хранения и подготовки тестовых данных.
- Автоматическое создание скриншотов при падении тестов.
- Параллельный запуск через pytest-xdist.

## Установка и запуск

Клонировать репозиторий:

```bash
git clone <URL репозитория>
cd youtrack_tests
```

Установить зависимости:

```bash
uv sync
```

Создать файл `.env` в корне проекта:

```env
YOUTRACK_USERNAME=your_username
YOUTRACK_PASSWORD=your_password
```

Запустить YouTrack через Docker Compose:

```bash
docker compose up -d
```

По умолчанию приложение доступно по адресу:

`http://localhost:8080`

Запустить тесты:

```bash
uv run pytest -v
```

Параллельный запуск:

```bash
uv run pytest -n 2 -v
```

Проверка кода:

```bash
uv run ruff check .
uv run ruff format --check .
```

## Скриншоты

При падении теста автоматически сохраняется скриншот страницы в директории:

`artifacts/screenshots/`

## Структура проекта

```text
youtrack_tests/
├── pages/
│   ├── __init__.py
│   ├── login_page.py
│   └── issue_page.py
├── tests/
│   ├── test_auth.py
│   ├── test_issue.py
│   └── test_smoke.py
├── artifacts/
├── .env
├── .gitignore
├── compose.yaml
├── conftest.py
├── pyproject.toml
└── README.md
```
