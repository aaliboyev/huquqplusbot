from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import SimpleEventIsolation
from src.config.redis_queue import telegram_storage
from src.config.settings import settings
from src.routes.aiogram.private_router import router as private_router
from src.routes.aiogram.group_router import router as group_router
import backoff
from sulguk import AiogramSulgukMiddleware


bot = Bot(settings.BOT_TOKEN)
bot.session.middleware(AiogramSulgukMiddleware())
dp = Dispatcher(
    storage=telegram_storage,
    events_isolation=SimpleEventIsolation())
dp.include_router(private_router)
dp.include_router(group_router)


@backoff.on_exception(backoff.expo, Exception, max_tries=5, max_time=30)
async def set_bot_webhook():
    webhook_path = f"{settings.BOT_WEBHOOK_URL}/api/v1/"
    current_url = await bot.get_webhook_info()
    if current_url.url != webhook_path:
        await bot.delete_webhook()
        await bot.set_webhook(url=webhook_path)
        print("Telegram webhook set successfully")
    else:
        print("Telegram webhook already set")
