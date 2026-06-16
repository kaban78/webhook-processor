# Webhook Processor

Платформа для приёма и асинхронной обработки веб-хуков.

## Архитектура

- **Flask** — принимает HTTP-запросы (POST /hook)
- **Redis** — очередь сообщений и хранилище статусов
- **Worker** — фоновая обработка задач

## Быстрый старт

```bash
# Зависимости
pip install -r requirements.txt

# Терминал 1: Redis
redis-server

# Терминал 2: Flask
python app.py

# Терминал 3: Worker
python worker.py

# Тест
curl -X POST http://localhost:5000/hook -H "Content-Type: application/json" -d '{"event":"test"}'
