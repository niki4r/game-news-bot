import os
import asyncio
from telegram import Bot
from news_fetcher import fetch_daily_news, generate_image

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)

async def test():
    print("Бот запускается...")
    try:
        text = await fetch_daily_news()
        print("Новости сформированы.")
        image = await generate_image()
        print("Картинка сгенерирована." if image else "Картинка не сгенерирована.")

        if image:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=image, caption="🎮 Вечерняя игровая сводка", parse_mode="HTML")
            await asyncio.sleep(2)  # ⏱ Задержка перед текстом, чтобы Telegram не завис
            await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="HTML")
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="HTML")

        print("Публикация завершена.")
    except Exception as e:
        print(f"Ошибка при выполнении: {e}")

if __name__ == "__main__":
    asyncio.run(test())
