# 💰 SmartBudget

Личный финансовый трекер с AI-категоризацией расходов.

## 🚀 Возможности

- Telegram бот для записи расходов
- AI автоматически определяет категорию (Llama 3.1)
- REST API на FastAPI
- Веб-дашборд на Django
- Хранение данных в PostgreSQL

## 🛠 Технологии

- **FastAPI** — REST API
- **Django** — веб-дашборд
- **Aiogram 3** — Telegram бот
- **SQLAlchemy** — работа с БД
- **PostgreSQL** — база данных
- **Redis** — кэш и очереди
- **Celery** — фоновые задачи
- **Docker** — контейнеризация
- **Groq/Llama 3.1** — AI категоризация

## ⚡ Быстрый старт

1. Клонируй репозиторий:
```bash
git clone https://github.com/Kamkines/smartbudget.git
cd smartbudget
```

2. Создай `.env` файл:
```bash
cp .env.example .env
# заполни данными
```

3. Запусти проект:
```bash
docker-compose up --build
```

4. API доступен на `http://localhost:8000/docs`

## 📁 Структура проекта
```
smartbudget/
├── services/
│   ├── api/          # FastAPI сервис
│   ├── web/          # Django дашборд
│   └── bot/          # Telegram бот
├── shared/           # Общие модули
├── docker-compose.yml
└── README.md
```