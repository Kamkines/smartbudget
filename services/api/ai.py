from groq import Groq
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()

client = Groq(api_key=settings.groq_api_key)

CATEGORIES = {
    "кафе и рестораны": "☕",
    "продукты": "🛒",
    "транспорт": "🚗",
    "развлечения": "🎮",
    "здоровье": "💊",
    "одежда": "👕",
    "коммунальные услуги": "🏠",
    "другое": "💰"
}

async def categorize_expense(description: str) -> str:
    categories_list = ", ".join(CATEGORIES.keys())
    
    prompt = f"""Определи категорию расхода из списка: {categories_list}

Расход: {description}

Ответь ТОЛЬКО названием категории из списка, без объяснений."""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20,
        temperature=0.1
    )
    
    category = completion.choices[0].message.content.strip().lower()
    print(f"AI категория: {category}")
    
    for cat_name in CATEGORIES.keys():
        if cat_name in category:
            return cat_name
    
    return "другое"