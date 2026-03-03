from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

# Таблица Пользователей
class User(Base): 
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Связь с транзакциями
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")

# Таблица Категорий
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    emoji: Mapped[str] = mapped_column(String(10))
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    # Связь с транзакциями
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category")

# Таблица Транзакций
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    description: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Внешние ключи - связи с другими таблицами
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) # Ссылка на юзера
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id")) # Ссылка на категорию

    # Связи
    user: Mapped["User"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")