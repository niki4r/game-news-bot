import feedparser
import openai
import os
from io import BytesIO
import base64
import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

FEEDS = [
    "https://www.ign.com/articles?format=rss",
    "https://www.gamespot.com/feeds/news/",
    "https://www.pushsquare.com/feeds/all"
]

async def fetch_daily_news():
    print("Получение новостей...")
    entries = []
    for feed in FEEDS:
        d = feedparser.parse(feed)
        entries += d.entries[:4]
    entries = entries[:9]
    print(f"Собрано {len(entries)} новостей.")

    summaries = []
    for i, e in enumerate(entries, 1):
        prompt = f"Сформулируй на русском короткую новость (1-2 предложения):\nЗаголовок: {e.title}\nОписание: {e.get('summary', '')}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            text = response["choices"][0]["message"]["content"].strip()
            print(f"GPT ответ {i}: {text[:60]}...")
        except Exception as ex:
            print(f"[Ошибка GPT для новости {i}]: {ex}")
            text = f"{e.title}"
        summaries.append(f"📰 <b>{text}</b>")

    today = datetime.datetime.now().strftime("%d.%m.%Y")
    full_text = f"🎮 <b>Вечерняя игровая сводка — {today}</b>\n\n" + "\n\n".join(summaries)
    return full_text

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