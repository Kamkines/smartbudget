from pathlib import Path
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    postgres_db: str = "smartbudget"
    postgres_user: str = "smartbudget_user"
    postgres_password: str = "supersecretpassword123"
    django_secret_key: str = "django-secret-key"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = settings.django_secret_key
DEBUG = settings.debug

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [ # какие приложения подключены
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "smartbudget.dashboard",
]

MIDDLEWARE = [  # цепочка обработчиков запроса
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "smartbudget.urls"

TEMPLATES = [ # где искать HTML шаблоны
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "smartbudget" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = { # подключение к БД
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.postgres_db,
        "USER": settings.postgres_user,
        "PASSWORD": settings.postgres_password,
        "HOST": "db",
        "PORT": "5432",
    }
}

STATIC_URL = "/static/" # где лежат CSS/JS файлы
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"