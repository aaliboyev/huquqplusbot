from aiogram.types import Update
from fastapi import APIRouter, Request
import traceback
from src.config.bot import dp, bot
from src.config.settings import settings
from src.routes.deps.db_session import DBSession

api_router = APIRouter()


@api_router.post("/")
async def root(update: Update, db_session: DBSession, request: Request):
    if request.headers.get("x-telegram-bot-api-secret-token", "") != settings.SECRET_KEY:
        return {
            "success": False,
            "error": "Invalid token"
        }

    try:
        await dp.feed_update(bot, update, db_session=db_session)
    except Exception as e:
        print(update)
        print(traceback.format_exc())
        print("Failed to handle update", e)
    return {"ok": True}


@api_router.get("/")
async def home_function():
    return {"ok": "Works as expected"}
