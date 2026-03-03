import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    telegram_bot_token: str
    api_url: str = "http://api:8000"

    class Config:
        env_file = ".env"

settings = Settings()

bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher() # диспетчер, распределяет входящие сообщения по обработчикам

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я помогу тебе отслеживать расходы.\n\n"
        "Просто напиши мне:\n"
        "💰 <сумма> <описание>\n\n"
        "Например: 500 кофе в старбаксе"
    )

    async with aiohttp.ClientSession() as session:     # Регистрируем пользователя в нашем API
        await session.post(
            f"{settings.api_url}/users/",
            json={
                "telegram_id": message.from_user.id,
                "username": message.from_user.username or message.from_user.first_name
            }
        )

# Обработчик сообщений с тратами
@dp.message(F.text) # срабатывает на любое текстовое сообщение.
async def handle_expense(message: Message):
    text = message.text.strip()

    # Парсим сообщение - первое слово это сумма, остальное описание
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("❌ Напиши в формате: 500 кофе в старбаксе")
        return

    try:
        amount = float(parts[0].replace(",", "."))
        description = parts[1]
    except ValueError:
        await message.answer("❌ Первым словом должна быть сумма. Например: 500 кофе")
        return

    await message.answer("⏳ Записываю...") 

    # Отправляем в наш API
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{settings.api_url}/transactions/",
            json={
                "amount": amount,
                "description": description,
                "telegram_id": message.from_user.id,
                "category_id": 1
            }
        )

        if response.status == 200:
            await message.answer(f"✅ Записал! {amount}р — {description}")
        else:
            await message.answer("❌ Что-то пошло не так, попробуй ещё раз")

async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)  # Polling — бот каждые несколько секунд спрашивает у Telegram "есть новые сообщения?" и обрабатывает их

if __name__ == "__main__":
    asyncio.run(main())