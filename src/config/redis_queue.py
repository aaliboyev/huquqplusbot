from aiogram.fsm.storage.redis import RedisStorage
from src.database.redisdb import get_redis

telegram_storage = RedisStorage(get_redis())
