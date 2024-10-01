from datetime import datetime
from sqlmodel import select
from sulguk import SULGUK_PARSE_MODE
from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from src.app.enums import disability_types, disability_states, regions, create_user_info
from src.app.filters import is_private_message
from src.app.keyboards import get_main_menu
from src.models.user import GenderType, User
from src.routes.deps.db_session import DBSession

registration_router = Router()


class RegistrationState(StatesGroup):
    first_name = State()
    last_name = State()
    middle_name = State()
    gender = State()
    birth_year = State()
    phone = State()
    disability_type = State()
    disability_state = State()
    region = State()


@registration_router.message(F.text == "🪪 Profil", is_private_message)
async def profile(message: Message, db_session: DBSession):
    kb = ReplyKeyboardBuilder()
    user = db_session.exec(select(User).where(User.user_id == message.from_user.id)).first()
    if user is None:
        return

    user_info = create_user_info(user, False)
    kb.button(text="🪪 O‘zgartirish")
    kb.button(text="⬅️ Asosiy menyu")
    await message.answer(
        "<p>Sizning profilingiz.</p>" + user_info,
        reply_markup=kb.adjust(2).as_markup(resize_keyboard=True),
        parse_mode=SULGUK_PARSE_MODE
    )


@registration_router.message(F.text == "❌ Bekor qilish", is_private_message)
@registration_router.message(F.text == "⬅️ Asosiy menyu", is_private_message)
async def profile(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Asosiy menyu", reply_markup=get_main_menu())


@registration_router.message(F.text == "🪪 O‘zgartirish", is_private_message)
async def start_registration(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.first_name)
    kb = ReplyKeyboardBuilder()
    kb.button(text="❌ Bekor qilish")
    await message.answer(
        "<b>Ismingizni kiriting...</b><br/><p>Masalan: Aziz</p>",
        reply_markup=kb.as_markup(resize_keyboard=True),
        parse_mode=SULGUK_PARSE_MODE
    )


@registration_router.message(RegistrationState.first_name, is_private_message)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(RegistrationState.last_name)
    kb = ReplyKeyboardBuilder()
    kb.button(text="❌ Bekor qilish")
    await message.answer("<b>Familiyangizni kiriting...</b><br><p>Masalan: Azizov</p>",
                         reply_markup=kb.as_markup(resize_keyboard=True),
                         parse_mode=SULGUK_PARSE_MODE)


@registration_router.message(RegistrationState.last_name, is_private_message)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(RegistrationState.gender)
    markup = ReplyKeyboardBuilder()
    markup.button(text="👦🏻 Erkak")
    markup.button(text="👧🏻 Ayol")
    markup.button(text="❌ Bekor qilish")
    await message.answer("Jinsingizni tanlang...",
                         reply_markup=markup.adjust(2).as_markup(resize_keyboard=True))


@registration_router.message(RegistrationState.gender, is_private_message)
async def get_gender(message: Message, state: FSMContext):
    if ['👦🏻 Erkak', '👧🏻 Ayol'].count(message.text) == 0:
        return await message.reply("Iltimos jinsingizni tanlang")
    await state.update_data(gender=GenderType.male if message.text == "👦🏻 Erkak" else GenderType.female)
    await state.set_state(RegistrationState.birth_year)
    kb = ReplyKeyboardBuilder()
    kb.button(text="❌ Bekor qilish")
    await message.answer("<b>Tug‘ilgan yilingizni kiriting...</b><br/><p>Masalan: 2000</p>",
                         reply_markup=kb.as_markup(resize_keyboard=True), parse_mode=SULGUK_PARSE_MODE)


@registration_router.message(RegistrationState.birth_year, is_private_message)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 1900 or int(message.text) > datetime.now().year:
        return await message.reply("Iltimos tug'ilgan yilingizni to'g'ri formatda kiriting")
    await state.update_data(birth_year=message.text)
    await state.set_state(RegistrationState.phone)
    markup = ReplyKeyboardBuilder()
    markup.button(text="📲 Telefon raqamini yuborish", request_contact=True)
    markup.button(text="❌ Bekor qilish")
    await message.answer("<b>Iltimos telefon raqamingizni yuboring...</b><br/>"
                         "<p>Pastki menyuda <b>\"Telefon raqamini yuborish\"</b> tugmasini bosing.<p>",
                         reply_markup=markup.as_markup(resize_keyboard=True), parse_mode=SULGUK_PARSE_MODE)


@registration_router.message(RegistrationState.phone, is_private_message)
async def get_phone(message: Message, state: FSMContext):
    print("phone", F.is_(ContentType.CONTACT))
    if not message.contact:
        return await message.reply("Iltimos telefon raqamingizni yuboring")
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(RegistrationState.disability_type)

    markup = ReplyKeyboardBuilder()
    for key, value in disability_types.items():
        markup.button(text=value)
    markup.button(text="❌ Bekor qilish")
    await message.answer(
        "Nogironlik guruhingizni tanlang...", reply_markup=markup.adjust(2).as_markup(resize_keyboard=True))


@registration_router.message(RegistrationState.disability_type, is_private_message)
async def get_disability_type(message: Message, state: FSMContext):
    if list(disability_types.values()).count(message.text) == 0:
        return await message.reply("Iltimos, nogironlik guruhingizni to'g'ri tanlang")

    disability_type = list(disability_types.keys())[list(disability_types.values()).index(message.text)]
    await state.update_data(disability_type=disability_type)
    await state.set_state(RegistrationState.disability_state)

    markup = ReplyKeyboardBuilder()
    for key, value in disability_states.items():
        markup.button(text=value)
    markup.button(text="❌ Bekor qilish")
    await message.answer("Nogironlik holatingizni tanlang...", reply_markup=markup.adjust(2).as_markup())


@registration_router.message(RegistrationState.disability_state, is_private_message)
async def get_disability_state(message: Message, state: FSMContext):
    if list(disability_states.values()).count(message.text) == 0:
        return await message.reply("Iltimos, nogironlik holatiingizni to'g'ri kiriting")

    disability_state = list(disability_states.keys())[list(disability_states.values()).index(message.text)]
    await state.update_data(disability_state=disability_state)
    await state.set_state(RegistrationState.region)

    markup = ReplyKeyboardBuilder()
    for key, value in regions.items():
        markup.button(text=value)
    markup.button(text="❌ Bekor qilish")
    await message.answer("Qayerdan ekanligingizni tanlang:", reply_markup=markup.adjust(2).as_markup())


@registration_router.message(RegistrationState.region, is_private_message)
async def get_region(message: Message, state: FSMContext, db_session: DBSession):
    if list(regions.values()).count(message.text) == 0:
        return await message.reply("Iltimos, hududingizni to'g'ri kiriting")

    await state.update_data(region=message.text)
    data = await state.get_data()

    existing_user = User.get_by_user_id(message.from_user.id, db_session)
    if not existing_user:
        user = User.model_validate({**data, 'user_id': message.from_user.id, 'username': message.from_user.username})
    else:
        user = existing_user
        user.sqlmodel_update(user, update={**data, 'user_id': message.from_user.id, 'username': message.from_user.username})
    db_session.add(user)
    db_session.commit()

    await state.clear()
    await message.answer("✅ Ma’lumotlaringiz qabul qilindi. Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!",
                         reply_markup=get_main_menu())
