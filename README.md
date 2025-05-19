# Game News Bot 🤖

Автоматический бот для Telegram, публикующий ежедневные игровые новости с изображением.

## Возможности

- Парсит новости с GameSpot, IGN, PushSquare, PureXbox, Eurogamer
- Переводит на русский с кратким описанием (GPT-4o)
- Генерирует тематическое изображение (OpenAI DALL·E)
- Публикует в Telegram в 20:00 по МСК

## Установка и запуск на Railway

1. Форкни или склонируй репозиторий
2. Добавь переменные окружения:

```
OPENAI_API_KEY=sk-...
TELEGRAM_BOT_TOKEN=bot...
TELEGRAM_CHANNEL_ID=@your_channel
```

3. Railway автоматически установит зависимости и запустит `main.py`

## Локальный запуск

```
pip install -r requirements.txt
python main.py
```

> Не забудь создать `.env` файл локально с нужными ключами.
