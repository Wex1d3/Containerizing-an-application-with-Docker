# KT. Контейнеризация и автоматический деплой

Учебный FastAPI-проект с PostgreSQL, Redis, Docker Compose и GitHub Actions.

## Состав проекта

- `app` — FastAPI на порту 8000;
- `db` — PostgreSQL 16;
- `redis` — Redis 7;
- `.github/workflows/tests.yml` — запуск pytest при push в `main`.

Внутри Docker-сети приложение обращается к сервисам по именам `db` и `redis`, а не через `localhost`.

## Запуск на Windows (CMD) или Linux

Установи и запусти Docker Desktop (Windows) либо Docker Engine и Docker Compose (Linux).

Перейди в папку проекта:
```cmd
cd путь\к\kt_containerization
```

Собери образы и запусти контейнеры:
```cmd
docker compose up --build
```

Открой в браузере:
- http://localhost:8000/
- http://localhost:8000/docs
- http://localhost:8000/health

`/health` проверяет фактическое подключение приложения к PostgreSQL и Redis.

Остановить контейнеры:
```cmd
docker compose down
```

Остановить контейнеры и удалить данные PostgreSQL:
```cmd
docker compose down -v
```

## Проверка тестов локально

```cmd
python -m pip install -r requirements.txt
python -m pytest -v
```

## GitHub Actions

Создай репозиторий на GitHub, загрузи файлы проекта и отправь изменения в ветку `main`:
```cmd
git init
git add .
git commit -m "KT containerization project"
git branch -M main
git remote add origin https://github.com/ВАШ_ЛОГИН/ВАШ_РЕПОЗИТОРИЙ.git
git push -u origin main
```

После push открой вкладку **Actions** репозитория. Workflow `Tests` автоматически выполнит `pytest`.

## Публичный деплой на VPS

Для выполнения пункта о публичном адресе нужен собственный VPS и доступ по SSH. На сервере установи Docker и Docker Compose, скопируй проект, затем выполни:
```bash
docker compose up --build -d
```

Разреши входящие подключения к порту 8000 в firewall VPS и проверь:
```bash
curl http://IP_ТВОЕГО_СЕРВЕРА:8000/docs
```

После успешного деплоя замени строку ниже на реальный адрес сервера:

**Публичный адрес приложения:** `НЕ ЗАДЕПЛОЕНО — добавьте URL после публикации`

Не указывай localhost в качестве публичного адреса. Не публикуй `.env.docker` с реальными паролями в открытом репозитории; для настоящего сервера используй секреты и надёжные пароли.

## Примечание

Это рабочий минимальный шаблон FastAPI для демонстрации контейнеризации и подключения к PostgreSQL/Redis. Если в предыдущих разделах у тебя уже есть собственные модели, маршруты и бизнес-логика, перенеси их в этот проект, сохранив Docker-конфигурацию и переменные окружения.
