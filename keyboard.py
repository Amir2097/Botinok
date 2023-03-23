from aiogram import types


buttons_cmd_random = [
        types.InlineKeyboardButton(text="📋 БОТИНОК для заметок", callback_data="botinok_info_notes"),
        types.InlineKeyboardButton(text="✅ Мероприятия", callback_data="events_data"),
        types.InlineKeyboardButton(text="🌪 Погодный ботинок", callback_data="weather_start")
    ]
keyboard_cmd_random = types.InlineKeyboardMarkup(row_width=2)
keyboard_cmd_random.add(*buttons_cmd_random)

buttons_weather = [
        types.InlineKeyboardButton(text="🌪 Погода сейчас", callback_data="weather"),
        types.InlineKeyboardButton(text="👞 ПРОГНОЗ НА 5 ДНЕЙ", callback_data="weather_long")
    ]
keyboard_weather_long = types.InlineKeyboardMarkup(row_width=2)
keyboard_weather_long.add(*buttons_weather)


buttons_send_random_value = [
        types.InlineKeyboardButton(text="📋 Новая заметка", callback_data="new_notes"),
        types.InlineKeyboardButton(text="💼 Мои заметки", callback_data="my_notes")
    ]
keyboard_send_random_value = types.InlineKeyboardMarkup(row_width=3)
keyboard_send_random_value.add(*buttons_send_random_value)


buttons_event = [
        types.InlineKeyboardButton(text="Настройки", callback_data="setting"),
        types.InlineKeyboardButton(text="Данные", callback_data="ext_data_event")
    ]
keyboard_event = types.InlineKeyboardMarkup(row_width=3)
keyboard_event.add(*buttons_event)


buttons_event_settings = [
            types.InlineKeyboardButton(text="Редактировать город", callback_data="city_edit"),
        ]
keyboard_event_settings = types.InlineKeyboardMarkup(row_width=3)
keyboard_event_settings.add(*buttons_event_settings)


buttons_new_notes_add = [
        types.InlineKeyboardButton(text="✍️ Редактировать", callback_data="edit_notes"),
        types.InlineKeyboardButton(text="❌ Удалить", callback_data="delete_notes")
    ]
keyboard_new_notes_add = types.InlineKeyboardMarkup(row_width=2)
keyboard_new_notes_add.add(*buttons_new_notes_add)



