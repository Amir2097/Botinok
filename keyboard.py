from aiogram import types
from Database import return_city


buttons_cmd_random = [
        types.InlineKeyboardButton(text="📋 Заметки", callback_data="botinok_info_notes"),
        types.InlineKeyboardButton(text="✅ Мероприятия", callback_data="events_data"),
        types.InlineKeyboardButton(text="🌪 Погодный ботинок", callback_data="weather_start"),
        types.InlineKeyboardButton(text="☯️ Гороскоп", callback_data="horoscope")
    ]
keyboard_cmd_random = types.InlineKeyboardMarkup(row_width=2)
keyboard_cmd_random.add(*buttons_cmd_random)

buttons_weather = [
        types.InlineKeyboardButton(text="⏳ Погода сейчас", callback_data="weather"),
        types.InlineKeyboardButton(text="🌎 НА 5 ДНЕЙ", callback_data="weather_long")
    ]
keyboard_weather_long = types.InlineKeyboardMarkup(row_width=2)
keyboard_weather_long.add(*buttons_weather)

buttons_weather_another = [
        types.InlineKeyboardButton(text="🏙 Другой город", callback_data="weather_city"),
        types.InlineKeyboardButton(text="🔙 В начало", callback_data="returnstart")
    ]
keyboard_weather_another = types.InlineKeyboardMarkup(row_width=2)
keyboard_weather_another.add(*buttons_weather_another)

buttons_send_random_value = [
        types.InlineKeyboardButton(text="📋 Новая заметка", callback_data="new_notes"),
        types.InlineKeyboardButton(text="💼 Мои заметки", callback_data="my_notes")
    ]
keyboard_send_random_value = types.InlineKeyboardMarkup(row_width=3)
keyboard_send_random_value.add(*buttons_send_random_value)


buttons_event = [
        types.InlineKeyboardButton(text="⚙️ Настройки", callback_data="setting"),
        types.InlineKeyboardButton(text="🎬 Мероприятия", callback_data="ext_data_event"),
        types.InlineKeyboardButton(text="🔙 В начало", callback_data="returnstart")
    ]
keyboard_event = types.InlineKeyboardMarkup(row_width=2)
keyboard_event.add(*buttons_event)


buttons_event_settings = [
        types.InlineKeyboardButton(text="✍️ Редактировать город", callback_data="city_edit"),
        types.InlineKeyboardButton(text="🏘️ НАЗАД", callback_data="events_data")
        ]
keyboard_event_settings = types.InlineKeyboardMarkup(row_width=1)
keyboard_event_settings.add(*buttons_event_settings)


buttons_new_notes_add = [
        types.InlineKeyboardButton(text="✍️ Редактировать", callback_data="edit_notes"),
        types.InlineKeyboardButton(text="❌ Удалить", callback_data="delete_notes")
    ]
keyboard_new_notes_add = types.InlineKeyboardMarkup(row_width=2)
keyboard_new_notes_add.add(*buttons_new_notes_add)

buttons_horo = [
        types.InlineKeyboardButton(text="♈️ Овен", callback_data="aries"),
        types.InlineKeyboardButton(text="♉️ Телец", callback_data="taurus"),
        types.InlineKeyboardButton(text="♊️ Близнецы", callback_data="gemini"),
        types.InlineKeyboardButton(text="♋️ Рак", callback_data="cancer"),
        types.InlineKeyboardButton(text="♌️ Лев", callback_data="leo"),
        types.InlineKeyboardButton(text="♍️ Дева", callback_data="virgo"),
        types.InlineKeyboardButton(text="♎️ Весы", callback_data="libra"),
        types.InlineKeyboardButton(text="♏️ Скорпион", callback_data="scorpio"),
        types.InlineKeyboardButton(text="♐️ Стрелец", callback_data="sagittarius"),
        types.InlineKeyboardButton(text="♑️ Козерог", callback_data="capricorn"),
        types.InlineKeyboardButton(text="♒️ Водолей", callback_data="aquarius"),
        types.InlineKeyboardButton(text="♓️ Рыбы", callback_data="pisces"),
    ]
keyboard_horo = types.InlineKeyboardMarkup(row_width=3)
keyboard_horo.add(*buttons_horo)


new_list = ["aries", "taurus"]

