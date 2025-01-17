from datetime import timedelta


CELERYBEAT_SCHEDULE = {
    "every-minute": {"task": "app.runcelery", "schedule": timedelta(seconds=60 * 5)}
}
# MONGO_URI = 'mongodb://dapdap:dapdapmima123@172.31.135.89:27017/dapdap'
MONGO_URI = "mongodb://127.0.0.1:27014/tt"
CELERY_BROKER_URL = ("redis://localhost:6379",)
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CACHE_REDIS_HOST = "127.0.0.1"
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 10
