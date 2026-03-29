# Легенды Острова

Базовый монолитный Django-проект для публикации художественных текстов с локализацией, премодерацией комментариев и встроенной админкой.

## Что есть на первом этапе

- Django-проект c `src/`-layout
- PostgreSQL в Docker Compose
- Разделённые настройки `base / local / production`
- Приложения `core`, `legends`, `comments`
- Модели легенд, переводов и комментариев
- Премодерация комментариев и журнал событий модерации
- Базовая главная страница и `/health/`
- Подготовка статики, медиа и i18n
- Django admin для публикации и модерации

## Требования

- Docker
- Docker Compose

Локальный Python не нужен: весь запуск и служебные команды выполняются внутри контейнера.

## Быстрый старт

1. Скопируй пример переменных окружения:

```powershell
Copy-Item .env.example .env
```

2. Собери и запусти проект:

```powershell
docker compose up --build
```

3. Открой в браузере:

- сайт: `http://localhost:8000/`
- английская версия: `http://localhost:8000/en/`
- healthcheck: `http://localhost:8000/health/`
- админка: `http://localhost:8000/admin/`

Контейнер `web` при старте ждёт готовности PostgreSQL и автоматически применяет миграции.

## Основные команды

### Запуск

```powershell
docker compose up --build
```

### Остановить окружение

```powershell
docker compose down
```

### Применить миграции вручную

```powershell
docker compose exec web python manage.py migrate
```

### Создать новые миграции

```powershell
docker compose exec web python manage.py makemigrations
```

### Создать суперпользователя

```powershell
docker compose exec web python manage.py createsuperuser
```

### Проверить конфигурацию Django

```powershell
docker compose exec web python manage.py check
```

### Скомпилировать переводы после изменения `*.po`

```powershell
docker compose exec web python manage.py compilemessages
```

## Переменные окружения

Смотри файл [`.env.example`](.env.example). Ключевые параметры:

- `DJANGO_SETTINGS_MODULE`
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DJANGO_TIME_ZONE`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

## Структура проекта

```text
.
├── compose.yaml
├── docker/
│   └── web/
├── requirements/
├── src/
│   ├── apps/
│   │   ├── comments/
│   │   ├── core/
│   │   └── legends/
│   ├── config/
│   │   └── settings/
│   ├── locale/
│   ├── static/
│   └── templates/
├── .env.example
├── Makefile
└── README.md
```

## Как устроена модель данных

### `legends`

- `Series`
- `SeriesTranslation`
- `Province`
- `ProvinceTranslation`
- `Patron`
- `PatronTranslation`
- `Tag`
- `TagTranslation`
- `Legend`
- `LegendTranslation`

`Legend` хранит общую сущность публикации, а `LegendTranslation` хранит контент и SEO-поля для конкретного языка. Slug уникален в рамках `locale`.

Серии, провинции, покровители и теги также хранят переводы в отдельных таблицах. Публичные taxonomy URL теперь локализованы и используют slug перевода, а не базовой сущности.

### `comments`

- `Comment`
- `CommentModerationEvent`

Все комментарии создаются в статусе `pending` и должны быть промодерированы через Django admin.

## Что подготовлено под следующий этап

- production settings
- `production.txt` для отдельных зависимостей
- статика и медиа с выделенными путями
- журнал событий модерации
- структура, готовая к переходу на Gunicorn

## Замечания по текущему этапу

- Публичные аккаунты пользователей не добавлены.
- CAPTCHA и rate limiting пока не внедрены.
