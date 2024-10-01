import asyncio
from datetime import datetime, timedelta
from aiogram.exceptions import TelegramForbiddenError, TelegramAPIError, TelegramRetryAfter
import backoff
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from sqlmodel import Session, select
from src.app.keyboards import get_main_menu
from src.config.bot import bot
from src.config.celery_app import celery_app
from src.config.redis_queue import telegram_storage
from src.database.mysql import engine
from src.models.inquiry import Inquiry, InquiryStatus
from src.tasks.daily_reminder import InquiryType
from src.tasks.utils import async_celery_task


@async_celery_task(celery_app, name="close_inquiry")
async def close_idle_inquiries():
    with Session(engine) as session:
        inquiries: list[InquiryType] = session.exec(
            select(Inquiry).where(Inquiry.status == InquiryStatus.replied)).all()

        d = datetime.now() - timedelta(hours=4)
        for i in inquiries:
            if i.replied_at < d:
                i.close(cancelled=False, session=session, commit=False)

                storage_key = StorageKey(user_id=i.user_id, chat_id=i.user_id, bot_id=bot.id)
                user_state = FSMContext(storage=telegram_storage, key=storage_key)
                await user_state.clear()
                await close_inquiry(
                    bot=bot,
                    chat_id=i.user_id,
                    text="Murojaat muvofaqiyatli yakunlandi! Sizga yordam bera olganimizdan xursandmiz",
                    reply_markup=get_main_menu())

        session.commit()


@backoff.on_exception(backoff.fibo, Exception, max_tries=10)
async def close_inquiry(bot: bot, chat_id: int, text: str, reply_markup: str):
    try:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    except TelegramRetryAfter as e:
        # If we hit a rate limit, wait for the recommended time
        await asyncio.sleep(e.retry_after)
        await close_inquiry(bot, chat_id, text, reply_markup)  # Retry after the timeout
    except Exception as e:
        # Other exceptions
        print(f"Error occurred: {e}")
        return
