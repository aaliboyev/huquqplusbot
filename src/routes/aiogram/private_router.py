import re
from datetime import datetime, timedelta
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from sulguk import SULGUK_PARSE_MODE

from src.app.filters import is_private_message
from src.app.generate_report import generate_report
from src.app.keyboards import get_main_menu
from src.models.user import User
from src.routes.aiogram.inquiry import inquiry_router
from src.routes.aiogram.registration import RegistrationState, registration_router
from src.routes.deps.db_session import DBSession

router = Router()
router.include_routers(registration_router, inquiry_router)


@router.message(Command("start"), is_private_message)
async def start_command(message: Message, state: FSMContext, db_session: DBSession):
    await state.clear()
    user = User.get_by_user_id(message.from_user.id, db_session)
    if not user:
        await state.set_state(RegistrationState.first_name)
        await message.answer(
            "<b>Ismingizni kiriting...</b><br/>Masalan: Aziz",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=SULGUK_PARSE_MODE
        )
    else:
        await message.answer("Siz ro'yxatdan o'tgansiz", reply_markup=get_main_menu())


@router.message(Command("report"), is_private_message)
async def menu_command(message: Message):
    date_pattern = r"(\d{2}/\d{2}/\d{2})-(\d{2}/\d{2}/\d{2})"
    match = re.search(date_pattern, message.text)
    if '-' not in message.text:
        return

    try:
        start_date, end_date = match.groups()
        start_date = datetime.strptime(start_date, "%d/%m/%y")
        end_date = datetime.strptime(end_date, "%d/%m/%y")
        end_date = end_date + timedelta(days=1)
    except Exception as e:
        print(e)
        return await message.answer("Iltimos sanalarni to'g'ri kiriting. Masalan: 01/08/24-30/08/24")

    filename = generate_report((start_date, end_date))
    file = FSInputFile(filename)
    await message.answer_document(document=file)
