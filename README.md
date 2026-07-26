# Habit Tracker

Трекер полезных привычек с Telegram-уведомлениями.

Стек: Django, DRF, PostgreSQL, Redis, Celery, Docker, Nginx, GitHub Actions.

## Функциональность

- Регистрация и авторизация пользователей (JWT)
- CRUD для привычек
- Список публичных привычек
- Валидаторы (время выполнения ≤ 120 сек, периодичность 1-7 дней, связанная привычка ИЛИ вознаграждение)
- Telegram-уведомления через Celery
- Пагинация (5 привычек на страницу)
- Права доступа (пользователь видит только свои привычки, публичные — все)
- Документация API (Swagger/Redoc)

## Запуск через Docker

1. Скопируйте `.env.example` в `.env` и заполните переменные окружения:
   ```bash
   cp .env.example .env

2. Запустите контейнеры:
   ```bash
   docker compose up --build -d

3. Выполните миграции:
   ```bash
   docker compose exec web python manage.py migrate

4. Создайте суперпользователя:
   ```bash
   docker compose exec web python manage.py createsuperuser

5. Откройте http://localhost:8000

## Сервисы в Docker Compose

web — Django (порт 8000)

db — PostgreSQL 15 (порт 5432)

redis — Redis 7 (порт 6379)

celery — обработка фоновых задач

celery-beat — периодические задачи (напоминания)

nginx — веб-сервер (порт 80)

CI/CD (GitHub Actions)
При пуше в main автоматически:

Запускаются тесты (python manage.py test)

При успешных тестах — деплой на сервер через SSH

На сервере выполняется docker compose up --build -d, миграции, сбор статики

Секреты GitHub Actions
Для работы деплоя добавьте секреты в репозиторий:

SSH_HOST — IP-адрес сервера

SSH_USER — пользователь на сервере

SSH_KEY — приватный SSH-ключ

Эндпоинты API
POST /api/token/ — получение JWT токена

POST /api/register/ — регистрация

GET /api/habits/ — список привычек пользователя

GET /api/habits/public/ — публичные привычки

POST /api/habits/ — создание привычки

PUT /api/habits/{id}/ — редактирование

DELETE /api/habits/{id}/ — удаление

/swagger/ — документация API

/admin/ — админка Django


