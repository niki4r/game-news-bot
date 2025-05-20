import feedparser
import openai
import os
from io import BytesIO
import base64
import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

FEEDS = {
    "https://dtf.ru/rss/games": 12,  # приоритет
    "https://www.gamespot.com/feeds/news/": 6,
    "https://feeds.feedburner.com/ign/all": 6,
    "https://www.pushsquare.com/feeds/news": 6,
    "https://www.purexbox.com/feeds/news": 6,
    "https://www.eurogamer.net/rss": 6
}

async def fetch_daily_news():
    print("Получение новостей...")
    entries = []
    for feed, count in FEEDS.items():
        d = feedparser.parse(feed)
        entries += d.entries[:count]
    print(f"Собрано всего {len(entries)} новостей.")

    filtered = []
    for e in entries:
        text = (e.title + " " + e.get("summary", "")).lower()
        if "discount" in text or "скидка" in text or "sale" in text or "% off" in text:
            continue
        filtered.append(e)

    print(f"Оставлено {len(filtered)} новостей после фильтрации скидок.")

    news_with_links = []
    for i, e in enumerate(filtered):
        title = e.title
        summary = e.get("summary", "")[:300].replace("\n", " ")
        link = e.link
        news_with_links.append(f"{i+1}. {title} - {summary}\nСсылка: {link}")

    bulk_prompt = "\n\n".join(news_with_links)

    system_message = "Ты — редактор Telegram-канала по играм на PlayStation и Xbox."

    user_prompt = f"""Вот список новостей:

{bulk_prompt}

Выбери 10 самых интересных новостей про PlayStation и Xbox.
Не включай Nintendo, PC-only, фильмы, сериалы, мангу и т.п.
ИСКЛЮЧИ любые новости о скидках, распродажах и акциях.

Для каждой:
- Переведи заголовок на русский и выдели его жирным
- В начале поставь подходящее эмодзи: 🎮 (игра), 🛠 (обновление), 🔥 (релиз), 💬 (слух), 🧪 (бета), 🎂 (годовщина) и т.п.
- Кратко опиши (1–2 предложения, по-русски)
- В конце описания вставь <a href="ССЫЛКА">Читать далее</a>
- Не вставляй ссылку в формате https:// — только в <a href>

Формат:
🎮 <b>Заголовок</b>
Описание. <a href="ССЫЛКА">Читать далее</a>

Максимум — 3900 символов.
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

# Экранируем HTML в тексте, кроме тегов <b> и <a>
    from html import escape
    import re

    def clean_html(text):
        allowed_tags = re.compile(r'(<\/?b>|<a href="[^"]+">|<\/a>)')
        parts = allowed_tags.split(text)
        result = ""
        for part in parts:
            if allowed_tags.fullmatch(part):
                result += part
            else:
                result += escape(part)
        return result

    formatted_news = clean_html(formatted_news)
    except Exception as e:
        print(f"[Ошибка GPT при составлении сводки]: {e}")
        formatted_news = "Не удалось сгенерировать сводку."

    today = datetime.datetime.now().strftime("%d.%m.%Y")
    return f"🎮 <b>Вечерняя игровая сводка — {today}</b>\n\n" + formatted_news

async def generate_image():
    prompt = "Evening gaming news, PlayStation and Xbox focus, dark neon style, 3D illustration, game icons, controller"
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