# FoodPlan - Telegram Bot для планирования питания

Telegram-бот для рекомендации рецептов, планирования рациона и формирования списка покупок.

## Функциональность

- **Рекомендация рецептов** - автоматический подбор блюд на день
- **Учет предпочтений** - система лайков/дизлайков для персонализации
- **Список покупок** - автоматическая генерация списка ингредиентов
- **Контроль бюджета** - расчет стоимости блюд
- **Ограниченные замены** - возможность заменить рецепт (до 3 раз в день)
- **Черный список** - исключение нелюбимых блюд

## Структура проекта

**bot/**                # Основной код бота
- callbacks.py          # Коллбэки для кнопок
- commands.py           # Обработчики команд
- handlers.py           # Обработчики сообщений
- keyboards.py          # Клавиатуры бота
- settings.py           # Настройки бота
- strings.py            # Текстовые сообщения

**demodata/**           # Демо-данные

**food_plan/**          # Настройки Django проекта
- asgi.py               # ASGI конфигурация
- settings.py           # Настройки Django
- urls.py               # URL маршруты
- wsgi.py               # WSGI конфигурация

**food_plan_app/**      # Django приложение
- migrations/           # Миграции базы данных
- admin.py              # Админ-панель Django
- apps.py               # Конфигурация приложения
- db_requests.py        # Запросы к базе данных
- models.py             # Модели данных
- serializers.py        # Сериализаторы данных
- tests.py              # Тесты
- views.py              # Представления

**images/**             # Папка для изображений рецептов

**.gitattributes**      # Настройки Git

**.gitignore**          # Игнорируемые файлы Git

**manage.py**           # Скрипт управления Django

**requirements.txt**    # Зависимости проекта

**run_bot.py**          # Запуск бота

## Технологии

- **Python 3.x**
- **Django 5.2** - веб-фреймворк
- **python-telegram-bot** - библиотека для Telegram API
- **SQLite** - база данных (по умолчанию)
- **environs** - управление environment variables

## Быстрый старт

1. Установка зависимостей
```bash
pip install -r requirements.txt
```

2. Настройка окружения
Создайте файл `.env` в корне проекта:

BOT_TOKEN=ваш_telegram_bot_token
SECRET_KEY=ваш_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
LANGUAGE_CODE=ru-ru
TIMEZONE=Europe/Moscow

3. Настройка базы данных

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Создание суперпользователя

```bash
python manage.py createsuperuser
```

5. Запуск бота

```bash
python run_bot.py
```

6. Запуск Django сервера (для админки)

```bash
python manage.py runserver
```

## Администрирование

Доступ к админ-панели: http://localhost:8000/admin/

Поддерживаемые модели:

- **Пользователи** - пользователи бота
- **Рецепты** - база рецептов с ингредиентами
- **Ингредиенты** - список доступных ингредиентов
- **Единицы измерения** - граммы, штуки, мл и т.д.
- **Ежедневные рецепты** - персонализированные рекомендации

## Основные команды:

```bash
# Запуск тестов
python manage.py test

# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Запуск с отладкой
python run_bot.py
```

## Примечания

- Текущая версия - MVP с базовым функционалом
- База данных использует SQLite для простоты разработки