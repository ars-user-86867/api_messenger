# Тестовое задание API чатов и сообщений

## Технологический стек
* **Framework:** FastAPI
* **Database:** PostgreSQL (`asyncpg`)
* **ORM:** SQLAlchemy 2.0 
* **Migrations:** Alembic
* **Containerization:** Docker
* **Testing:** pytest / httpx / Transactional Rollbacks

## Функционал
- Создание чатов
- Добавление текстовых сообщений в чат
- Получение списка чатов с последними N сообщениями
- Удаление чата (каскадное удаление сообщений)
- Автоматические миграции БД при старте

## Требования
- Docker и Docker Compose
- Python 3.12 (для локального запуска)

## Структура проекта

- src/ — исходный код приложения
    
- deploy/ — конфигурация Docker и Docker Compose
    
- envs/ — файлы переменных окружения
    
- migrations/ — история миграций Alembic
    
- tests/ — тесты

## Запуск проекта

1. **Подготовка окружения:**
   В папке `envs/` есть шаблон `sample.env`, на основании которого нужно создать файл `.env`, и разместить в папке `envs/ 

2. **Сборка и запуск:**
   В корне проекта:
	1. запуск
        ```bash
        docker compose --env-file envs/.env -f deploy/docker-compose.yml up --build -d
        ```
	   Если не был указан другой порт для fastapi, то после запуска документация api доступна по ссылке http://localhost:8000/docs#
	2.  просмотр логов
        ```bash
        docker compose --env-file envs/.env -f deploy/docker-compose.yml logs -n 100 -f
        ```
	3. остановка
        ```bash
        docker compose --env-file envs/.env -f deploy/docker-compose.yml down
        ```



## Тестирование

Для запуска тестов используется pytest. Тест для проверки создания чата настроен на работу с изолированной тестовой базой данных и используют механизм транзакционного отката (rollback) после каждого теста. Тест запускаются локально. Также есть тест для проверки сборки конфига. Тесты не настроены для запуска в контейнере docker. Запуск тестов локально. 
Запуска тестов (локально):
```bash
pytest -v
```