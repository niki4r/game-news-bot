import feedparser
import openai
import os
from io import BytesIO
import base64
import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

FEEDS = [
    "https://www.gamespot.com/feeds/news/",
    "https://feeds.feedburner.com/ign/all",
    "https://www.pushsquare.com/feeds/news",
    "https://www.purexbox.com/feeds/news",
    "https://www.eurogamer.net/rss",
    "https://dtf.ru/rss/games"
]

async def fetch_daily_news():
    print("Получение новостей...")
    entries = []
    for feed in FEEDS:
        d = feedparser.parse(feed)
        entries += d.entries[:10]
    print(f"Собрано всего {len(entries)} новостей.")

    # Преобразуем список новостей в текст для GPT
    bulk_prompt = "\n".join([f"{i+1}. {e.title} - {e.get('summary', '')[:200]}" for i, e in enumerate(entries)])

    system_message = "Ты — редактор Telegram-канала про игры. Твоя задача — выбрать 10 самых важных и интересных новостей и оформить их в нужном формате. Без лишней воды."

    user_prompt = f"""Вот список новостей за день:

{bulk_prompt}

Выбери 10 самых интересных новостей. Для каждой напиши:
<b>Заголовок</b>
1–2 предложения с описанием. Источники не указывай. Пиши кратко, по делу. Уложись в 3900 символов. Не нумеруй.

Формат:

<b>Заголовок</b>
Описание.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        formatted_news = response["choices"][0]["message"]["content"].strip()

        if len(formatted_news) > 3900:
            formatted_news = formatted_news[:3900].rsplit("\n", 1)[0] + "\n…"

        print("Сводка сформирована.")
    except Exception as e:
        print(f"[Ошибка GPT при составлении сводки]: {e}")
        formatted_news = "Не удалось сгенерировать сводку."

    today = datetime.datetime.now().strftime("%d.%m.%Y")
    return f"🎮 <b>Вечерняя игровая сводка — {today}</b>\n\n" + formatted_news

async def generate_image():
    prompt = "Evening gaming news, PlayStation, Xbox, dramatic light, neon dark style"
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )
        image_data = base64.b64decode(response['data'][0]['b64_json'])
        print("Картинка успешно сгенерирована.")
        return BytesIO(image_data)
    except Exception as e:
        print(f"[Ошибка генерации изображения]: {e}")
        return None