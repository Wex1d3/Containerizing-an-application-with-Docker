import os

import psycopg2
import redis
from fastapi import FastAPI

app = FastAPI(title="KT: Контейнеризация и автоматический деплой")


def check_database() -> bool:
    connection = psycopg2.connect(os.environ["DATABASE_URL"], connect_timeout=3)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone()[0] == 1
    finally:
        connection.close()


def check_redis() -> bool:
    client = redis.Redis.from_url(
        os.environ["CELERY_BROKER"],
        socket_connect_timeout=3,
        socket_timeout=3,
    )
    return bool(client.ping())


@app.get("/")
def root():
    return {"message": "Hello from KT!", "status": "running"}


@app.get("/health")
def health():
    results = {}
    for service, check in (("database", check_database), ("redis", check_redis)):
        try:
            results[service] = "ok" if check() else "error"
        except Exception:
            results[service] = "error"

    status = "ok" if all(value == "ok" for value in results.values()) else "error"
    return {"status": status, "services": results}
