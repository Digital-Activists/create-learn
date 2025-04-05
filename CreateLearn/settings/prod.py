from .base import *

DEBUG = False
ALLOWED_HOSTS = ["your-domain.com"]  # замените на ваш домен

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "your_database_name",  # замените на имя базы данных
        "USER": "your_database_user",  # замените на пользователя базы данных
        "PASSWORD": "your_database_password",  # замените на пароль
        "HOST": "localhost",
        "PORT": "5432",
    }
}
