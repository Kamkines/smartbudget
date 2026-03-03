from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User, Transaction, Category
from schemas import UserCreate, UserResponse, TransactionCreate, TransactionResponse, CategoryCreate, CategoryResponse
from ai import categorize_expense

# Роутеры - это как мини-приложения внутри FastAPI
# prefix - это с чего должен начинаться эндпоинт
# tags - это нужно для группировки в сваггере
users_router = APIRouter(prefix="/users", tags=["Users"])
transactions_router = APIRouter(prefix="/transactions", tags=["Transactions"])
categories_router = APIRouter(prefix="/categories", tags=["Categories"])


# ===== ПОЛЬЗОВАТЕЛИ =====

@users_router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)): # Dependency Injection - это метод, благодаря которому мы автоматически получаем сессии из пула, используем их и возвращаем обратно в пул
    result = await db.execute(select(User).where(User.telegram_id == user.telegram_id))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    new_user = User(telegram_id=user.telegram_id, username=user.username)
    db.add(new_user)
    await db.flush()
    return new_user


# ===== КАТЕГОРИИ =====

@categories_router.post("/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    new_category = Category(name=category.name, emoji=category.emoji)
    db.add(new_category) # добавление в память Python
    await db.flush() # отправили в БД, объект получил id (тут можно откатить)
    # вот тогда данные сохранятся окончательно (когда закроется сессия - get_db закончится)
    return new_category

@categories_router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all() # scalars - получение данных, а all - помогает их распаковать

# ===== ТРАНЗАКЦИИ =====

@transactions_router.post("/", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.telegram_id == transaction.telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # AI определяет категорию автоматически
    category_name = await categorize_expense(transaction.description)
    
    # Ищем категорию в базе или создаём новую
    result = await db.execute(select(Category).where(Category.name == category_name))
    category = result.scalar_one_or_none()
    
    if not category:
        from ai import CATEGORIES
        emoji = CATEGORIES.get(category_name, "💰")
        category = Category(name=category_name, emoji=emoji)
        db.add(category)
        await db.flush()

    new_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        user_id=user.id,
        category_id=category.id
    )
    db.add(new_transaction)
    await db.flush()
    return new_transaction

@transactions_router.get("/{user_id}", response_model=list[TransactionResponse])
async def get_transactions(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transaction).where(Transaction.user_id == user_id))
    return result.scalars().all()