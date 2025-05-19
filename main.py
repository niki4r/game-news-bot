import os
import asyncio
from telegram import Bot
from news_fetcher import fetch_daily_news

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)

async def test():
    print("Бот запускается...")
    try:
        text = await fetch_daily_news()
        print("Новости сформированы.")

        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="HTML")
        print("Публикация завершена.")
    except Exception as e:
        print(f"Ошибка при выполнении: {e}")

if __name__ == "__main__":
    asyncio.run(test())
