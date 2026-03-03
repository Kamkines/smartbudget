from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker #SQLAlchemy - это инструмент, позволяющий язык питона переводит на язык SQL
from sqlalchemy.orm import DeclarativeBase
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    class Config:
        env_file = ".env"

settings = Settings()

# Создаём подключение к базе данных (echo = логирование запросов)
engine = create_async_engine(settings.database_url, echo=True)

# Фабрика сессий
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# Функция для получения сессии
async def get_db():
    async with SessionLocal() as session:
        async with session.begin():
            yield session