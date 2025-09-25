News Service API
Django REST API для управления новостями с документацией Swagger.
Структура проекта
news_service/
├── accounts/          # Управление пользователями
├── articles/          # CRUD операции со статьями
├── favorites/         # Избранные статьи
├── news_service/      # Основные настройки Django
├── db.sqlite3         # База данных SQLite
├── manage.py          # Django management скрипт
└── requirements.txt   # Зависимости
Установка

Создайте виртуальное окружение:

python -m venv env
source env/bin/activate  # Linux/Mac


Установите зависимости:

pip install -r requirements.txt

Выполните миграции:

python manage.py migrate

Создайте суперпользователя:

python manage.py createsuperuser

Запустите сервер:

python manage.py runserver
API Endpoints
Swagger документация

Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/
OpenAPI Schema: http://localhost:8000/swagger.json

Основные эндпоинты
Аутентификация

POST /api/auth/login/ - Вход
POST /api/auth/logout/ - Выход
POST /api/auth/register/ - Регистрация

Статьи

GET /api/articles/ - Список статей
POST /api/articles/ - Создать статью
GET /api/articles/{id}/ - Получить статью
PUT /api/articles/{id}/ - Обновить статью
DELETE /api/articles/{id}/ - Удалить статью

Избранное

GET /api/favorites/ - Избранные статьи
POST /api/favorites/ - Добавить в избранное
DELETE /api/favorites/{id}/ - Удалить из избранного

Django - Web framework
Django REST Framework - REST API
drf-yasg - Swagger/OpenAPI документация
SQLite - База данных

Разработка
Для добавления новых эндпоинтов обновите соответствующие ViewSets и сериализаторы. Документация Swagger обновится автоматически благодаря drf-yasg.
