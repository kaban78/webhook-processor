import asyncio
import json
from redis.asyncio import Redis
from config import settings

async def process_event(event: dict):
    print(f"Processing event: {event}")
    await asyncio.sleep(0.5)

async def main():
    redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    queue = settings.REDIS_QUEUE
    processing_queue = settings.REDIS_PROCESSING_QUEUE

    while True:
        task = await redis.brpoplpush(queue, processing_queue, timeout=0)
        try:
            event = json.loads(task)
            await process_event(event)
            await redis.lrem(processing_queue, 0, task)
        except Exception as e:
            print(f"Error processing task, left in {processing_queue}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
