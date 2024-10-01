from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

inquiry_sections = {
    '🛡  Ijtimoiy himoya': 1470,
    '👨🏻‍🎓 Ta’lim': 1441,
    '👩🏻‍💼 Mehnat': 1466,
    '🏘  Uy-joy': 1340,
    '🧑🏻‍⚕ Tibbiy xizmat va reabilitatsiya': 1349,
    '⚖️ Sud-huquq': 1477,
    '🚍 Transport': 1346,
    "🧒🏻 Bolalar": 1458,
    "🧑🏻 Yoshlar": 1451,
    "👩🏻 Ayollar": 1447,
    "🗒 Temir, yoshlar va ayollar daftari": 1355,
    "🏢 Tadbirkorlik": 1439
}


main_menu_items = {
    'profile': "🪪 Profil",
    'inquiry': "📩 Savol yuborish",
}


def get_main_menu():
    main_menu = ReplyKeyboardBuilder()
    for key, value in main_menu_items.items():
        main_menu.button(text=value)

    return main_menu.adjust(2).as_markup(resize_keyboard=True)


def inquiry_main_menu():
    main_menu = ReplyKeyboardBuilder()
    for key, value in inquiry_sections.items():
        main_menu.button(text=key)
    main_menu.button(text="⬅️ Asosiy menyu")
    return main_menu.adjust(2).as_markup(resize_keyboard=True)
