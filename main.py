from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from config import settings
from webhooks import router as webhook_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = mongo_client[settings.MONGODB_DB]
    await db.webhooks.create_index("received_at")
    await db.webhooks.create_index("event_type")
    app.state.db = db

    redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    app.state.redis = redis

    yield

    mongo_client.close()
    await redis.close()

app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router)
