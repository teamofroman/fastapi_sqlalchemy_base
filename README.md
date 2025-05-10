# Основа для проектов с FastAPI и SQLAlchemy

Базовый шаблон для проектов, основанных на FastAPI с использованием SQLAlchemy и подключением к БД Postgres.

## Структура проекта

Проект имеет следующую структуру:

```
├── README.md
├── infra
│   ├── .env.example
│   └── docker-compose.yml
├── requirements_style.txt
├── ruff.toml
├── src
│   ├── alembic.ini
│   ├── api
│   │   ├── __init__.py
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   ├── common.py
│   │   │   └── v1
│   │   │       ├── __init__.py
│   │   │       └── users.py
│   │   └── fastapi_app.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── config.py
│   │   └── db.py
│   ├── dao
│   │   ├── __init__.py
│   │   ├── base_dao.py
│   │   └── user_dao.py
│   ├── log
│   ├── main.py
│   ├── migrations
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── 2025_04_08_21_06-d108adeb32a1_add_user_model.py
│   ├── models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── requirements.txt
│   └── schemas
│       ├── __init__.py
│       └── user.py
└── tests
    └── api.http

```

Описание каталогов:
- **infra** - каталог с настройками проекта
- **src** - каталог с основными файлами проекта
- **tests** - каталог для размещения тестов

### Каталог `infra`

В каталоге располагаются файлы настроек и подготовки окружения для запуска проекта:
- **.env.example** - пример файла с настройками. На его основе должен быть создан файл `.env` с корректными настройками проекта.
- **docker-compose.yml** - файл для поднятия контейнеров проекта с использованием docker compose.

### Каталог `src`

В каталоге располагаются основные файлы проекта.

```
└── src
    ├── api                 Основной каталог FastAPI
    │   └── endpoints       Описание ендпоинтов (основные и версионные)
    │       └── v1          Обеспечение версионности ендпоинтов
    ├── core                Основные настроечные файлы (настройки, инициализации БД, базовая модель)
    ├── dao                 Файлы, обеспечивающие работу с данными БД
    ├── log                 Логи работы приложения
    ├── migrations          Файлы миграций Alembic
    ├── models              Описание моделей БД
    └── schemas             Описание схем данных для FastAPI на основе Pydantic
```
