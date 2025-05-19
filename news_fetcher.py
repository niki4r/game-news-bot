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
        entries += d.entries[:6]
    print(f"Собрано всего {len(entries)} новостей.")

    news_with_links = []
    for i, e in enumerate(entries):
        title = e.title
        summary = e.get("summary", "")[:300].replace("\n", " ")
        link = e.link
        news_with_links.append(f"{i+1}. {title} - {summary}\nСсылка: {link}")

    bulk_prompt = "\n\n".join(news_with_links)

    system_message = "Ты — редактор Telegram-канала, посвящённого играм для PlayStation и Xbox."

    user_prompt = f"""Вот список новостей:

{bulk_prompt}

Выбери 10 самых интересных новостей только для PlayStation (PS4, PS5) и Xbox. Не включай новости о:
- Nintendo
- PC-only играх
- манге, аниме, кино или сериалах

Ориентируйся на анонсы, скидки, релизы, обновления, утечки, бандлы. В начале каждой новости поставь эмодзи по смыслу (🎮, ⚔️, 📦, 💬, 📉, 🕹 и т.п.).

Формат:
🎮 <b>Заголовок</b>
Описание. Ссылка
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
    prompt = "Evening gaming news, PlayStation and Xbox focus, dramatic neon dark style"
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