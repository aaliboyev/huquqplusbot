from aiogram.types import Message
from src.config.settings import settings


def is_private_message(message):
    return message.chat.type == "private"


def is_group_message(message):
    return message.chat.type in ["group", "supergroup"]


def reply_to_my_message(message: Message):
    if not message.reply_to_message:
        return False
    return message.reply_to_message and message.reply_to_message.from_user.username == settings.BOT_NAME
