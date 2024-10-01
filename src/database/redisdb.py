from redis.asyncio.client import Redis as aioredis
import redis as rds
from src.config.settings import settings


def get_redis(is_async=True):
    if is_async:
        return aioredis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
            decode_responses=True, password=settings.REDIS_PASS, health_check_interval=30)
    else:
        return rds.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
                         decode_responses=True, password=settings.REDIS_PASS, health_check_interval=30)
