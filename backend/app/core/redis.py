from redis import asyncio as aioredis
from app.core.config import settings
from typing import Optional

redis_client: Optional[aioredis.Redis] = None


async def get_redis():
    """Get Redis client"""
    global redis_client
    if redis_client is None:
        redis_client = await aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    return redis_client


async def close_redis():
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()

