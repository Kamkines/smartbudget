# Устанавливаем Питон определенной версии
FROM python:3.12-slim

# Создание папки внутри контейнера
WORKDIR /app

# Копирование зависимостей/библиотек
COPY requirements.txt .

# Установление зависимостей/библиотек
RUN pip install --no-cache-dir -r requirements.txt

# Копирование
COPY . .

# Запуск
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]