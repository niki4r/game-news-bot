import os
import asyncio
import datetime
from telegram import Bot
from news_fetcher import fetch_daily_news, generate_image

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TZ_OFFSET = 3  # МСК

bot = Bot(token=BOT_TOKEN)

async def send_news():
    print("📤 Генерация новостной сводки...")
    try:
        text = await fetch_daily_news()
        image = await generate_image()
        if image:
            await bot.send_photo(chat_id=CHANNEL_ID, photo=image, caption="🎮 Вечерняя игровая сводка", parse_mode="HTML")
            await asyncio.sleep(2)
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="HTML")
        print("✅ Сводка успешно опубликована.")
    except Exception as e:
        print(f"[Ошибка при публикации]: {e}")

async def scheduler():
    while True:
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=TZ_OFFSET)
        if now.hour == 21 and now.minute == 0:
            await send_news()
            await asyncio.sleep(60)
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(scheduler())