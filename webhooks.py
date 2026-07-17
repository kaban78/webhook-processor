import json
from fastapi import APIRouter, Request, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from redis.asyncio import Redis
from config import settings
from signature import verify_signature
from models import webhook_document

router = APIRouter()

@router.post("/webhook")
async def receive_webhook(request: Request):
    raw_body = await request.body()
    event_type = request.headers.get("X-Event-Type", "unknown")
    signature_header = request.headers.get("X-Signature-256")

    if not verify_signature(settings.WEBHOOK_SECRET, raw_body, signature_header):
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    db: AsyncIOMotorDatabase = request.app.state.db
    doc = webhook_document(event_type, raw_body, payload)
    await db.webhooks.insert_one(doc)

    redis: Redis = request.app.state.redis
    await redis.lpush(settings.REDIS_QUEUE, json.dumps({
        "event_type": event_type,
        "payload": payload,
        "received_at": doc["received_at"].isoformat(),
    }))

    return {"status": "accepted"}
