from src.models.user import Region, User, GenderType


gender_types = {
    'male': 'Erkak',
    'female': 'Ayol',
}
disability_types = {
    'first_degree': '1⃣ Birinchi guruh',
    'second_degree': '2⃣ Ikkinchi guruh',
    'third_degree': '3⃣ Uchinchi guruh',
    'forth_degree': '4⃣ Toʻrtinchi guruh (18 yoshgacha nogironligi boʻlgan bola)',
    'none': '🚫 Nogironlik guruhi yoʻq',
}
disability_states = {
    'physical': '👩🏻‍🦽 Jismoniy nogironlik',
    'vision': '🧑🏻‍🦯 Ko‘rish bo‘yicha nogironlik',
    'hearing': '🧏🏻‍♀ Eshitish bo‘yicha nogironlik',
    'mental': '🧠 Aqliy nogironlik',
    'psychological': '❤️‍🩹 Ruhiy nogironlik',
    'parent': '👩🏻‍🍼Nogironligi bo‘lgan bolaning ota-onasi',
    'aids': '🩸OIV/OITS bo‘yicha nogironlik',
    'other': 'Boshqa',
}
regions = {region.name: region.value for region in Region}


def create_user_info(user: User, with_link=True):
    if not user.username:
        user_link = f'tg://user?id={user.user_id}'
    else:
        user_link = f'https://t.me/{user.username}'

    name = f"{user.first_name or ''} {user.last_name or ''}"

    user_str = f"""
        <b>Foydalanuvchi</b><br/>
        <b>Ismi:</b> {name}<br/>
        <b>Tug'ilgan yili:</b> {user.birth_year}<br/>
        <b>Jinsi:</b> {'Erkak' if user.gender == GenderType.male else 'Ayol'}<br/>
        <b>Hudud:</b> {regions[user.region.name]}<br/>
        <b>Nogironlik guruhi:</b> {disability_types[user.disability_type.value]}<br/>
        <b>Nogironlik holati:</b> {disability_states[user.disability_state.value]}<br/>
        <b>Telefon raqami:</b> {user.phone}<br/>
        """

    if with_link:
        user_str += f'<b><a href="{user_link}">Bog\'lanish uchun havola</a></b>'

    return user_str
