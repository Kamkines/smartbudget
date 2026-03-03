import os
import sys

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartbudget.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django") from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()

# manage.py - точка входа, команды django - как package.json scripts
# settings.py - конфиг всего проекта (БД, приложения, шаблоны)
# urls.py - роутинг, какой URL → какая view как роутер в FastAPI)
# wsgi.py - точка входа для сервера (как main.py в FastAPI)
# models.py - описание таблиц БД (как SQLAlchemy модели)
# views.py - логика страниц (как эндпоинты в FastAPI)
# index.html - HTML шаблон с данными