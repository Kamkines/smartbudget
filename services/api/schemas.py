#Это контракты для реквеста и респонса
from pydantic import BaseModel # Это валидатор данных, конфиги from_attributes = True нужны как раз для того, чтобы все было читабельно (не только из словарей, но и атрибут объектов)
from datetime import datetime
from decimal import Decimal

# Контракты для пользователя
class UserCreate(BaseModel):
    telegram_id: int
    username: str

class UserResponse(BaseModel):
    id: int
    telegram_id: int
    username: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Контракты для транзакции
class TransactionCreate(BaseModel):
    amount: Decimal
    description: str
    telegram_id: int  
    category_id: int

class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    description: str
    created_at: datetime
    user_id: int
    category_id: int

    class Config:
        from_attributes = True

# Контракты для категории
class CategoryCreate(BaseModel):
    name: str
    emoji: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    emoji: str

    class Config: 
        from_attributes = True

