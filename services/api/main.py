from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
from models import User, Category, Transaction
from routers import users_router, transactions_router, categories_router
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы созданы!")
    yield
    await engine.dispose()

# Сама Апишка
app = FastAPI(
    title="SmartBudget API",
    description="API для личного финансового трекера",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(users_router)
app.include_router(transactions_router)
app.include_router(categories_router)

# Первый эндпоинт, тестовый
@app.get("/")
def root():
    return {"message": "SmartBudget API работает! 🚀"}

# Второй эндпоинт, проверка работоспособности апишки
@app.get("/health")
def health():
    return {"status": "ok"}