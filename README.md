# API Wallet

## Технологии

- fastapi
- alembic
- asyncpg
- pydantic
- python-dotenv
- SQLAlchemy
- Nginx + uvicorn

## Для корректной работы в корне проекта создайте файл `.env` и заполните его по аналогии:

    DB_NAME=db_name
    DB_USER=db_user
    DB_PASSWORD=db_password
    DB_HOST=localhost
    DB_PORT=5432

## Для запуска требуется собрать контейнеры Docker и запустить их:

    docker-compose up -d --build

По умолчанию API работает на [localhost](http://localhost/)

Для удобной работы (с документацией) используйте [swagger](http://localhost/docs)

## Так же вне Docker имеются тесты для эндпоинтов, их можно запустить:

#1 Запуск сервера

    uvicorn main:app --reload

#2 Запуск тестов

    pytest -s tests/test_main.py -v

