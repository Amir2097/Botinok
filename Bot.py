from dotenv import load_dotenv
import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from Database import User, Notes, create_tables, user_entry, notes_new
from Database import session
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv("TOKEN"))

dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class ProfilStatesGroup(StatesGroup):
    text = State()

@dp.message_handler(commands="start")
async def cmd_random(message: types.Message):
    user_name = f"{message.from_user.first_name} {message.from_user.last_name}"
    user_entry(message.from_user.id, user_name, None, message.date)
    print(message)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="🤖 БОТИНОК для заметок 🤖", callback_data="botinok_start"))
    await message.answer("Привет!👋 Я БОТИНОК многофункциональный!🤖 Пока во мне реализованы заметки!✍️", reply_markup=keyboard)

@dp.callback_query_handler(text="botinok_start")
async def send_random_value(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="📋 Новая заметка", callback_data="new_notes"),
        types.InlineKeyboardButton(text="💼 Мои заметки", callback_data="my_notes"),
        types.InlineKeyboardButton(text="✍️ Редактирование", callback_data="edit_notes"),
        types.InlineKeyboardButton(text="👞 БОТИНОК", callback_data="botinok"),
        types.InlineKeyboardButton(text="❌ Удаление", callback_data="delete_notes"),
        types.InlineKeyboardButton(text="✅ Напоминание", callback_data="reminder_notes")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    await call.message.answer("БОТИНОК для ваших заметок.👞 Всегда под рукой!🤝"
                              "В меня вы можете записать все что угодно!🕵️‍♂️🧠", reply_markup=keyboard)


@dp.callback_query_handler(text="new_notes")
async def new_notes_add(message: types.Message) -> None:
    await message.answer("Напишите новую заметку ✍️!")
    await ProfilStatesGroup.text.set()  # Устанавливаем состояние

@dp.message_handler(state=ProfilStatesGroup.text)  # Принимаем состояние
async def new_notes_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:  # Устанавливаем состояние ожидания
        data['text'] = message.text
        subq = session.query(User.id).filter(User.id_tg == message.from_user.id).first()
        notes_new(data['text'], subq)
    await message.answer("Заметка готова ✍️!")
    await state.finish()





if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



