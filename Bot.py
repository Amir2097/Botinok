from dotenv import load_dotenv
import os
import logging
from Database import session
from dotenv import load_dotenv
from extraction import ext_events
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from Database import User, Notes, create_tables, user_entry, notes_new, city_edit

load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv("TOKEN"))

dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


class ProfilStatesGroup(StatesGroup):
    text = State()
    city = State()
    edit = State()


@dp.message_handler(commands="start")
async def cmd_random(message: types.Message):
    user_name = f"{message.from_user.first_name} {message.from_user.last_name}"
    user_entry(message.from_user.id, user_name, None, message.date)
    buttons = [
        types.InlineKeyboardButton(text="📋 БОТИНОК для заметок", callback_data="botinok_start"),
        types.InlineKeyboardButton(text="👞 БОТИНОК", callback_data="botinok"),
        types.InlineKeyboardButton(text="✅ Мероприятия", callback_data="events_data")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer("Привет!👋 Я БОТИНОК многофункциональный!🤖 Пока во мне реализованы заметки!✍️",
                         reply_markup=keyboard)


@dp.callback_query_handler(text="botinok_start")
async def send_random_value(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="📋 Новая заметка", callback_data="new_notes"),
        types.InlineKeyboardButton(text="💼 Мои заметки", callback_data="my_notes"),
        types.InlineKeyboardButton(text="✅ Напоминание", callback_data="reminder_notes")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    await call.message.answer("БОТИНОК для ваших заметок.👞 Всегда под рукой!🤝"
                              "В меня вы можете записать все что угодно!🕵️‍♂️🧠", reply_markup=keyboard)


@dp.callback_query_handler(text="events_data")
async def event(call: types.CallbackQuery):
    buttons = [
        types.InlineKeyboardButton(text="Настройки", callback_data="setting"),
        types.InlineKeyboardButton(text="Данные", callback_data="ext_data_event")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    await call.message.answer("Выбор действия", reply_markup=keyboard)

    @dp.callback_query_handler(text="ext_data_event")
    async def event_settings(call: types.CallbackQuery):
        pass

    @dp.callback_query_handler(text="setting")
    async def event_settings(call: types.CallbackQuery):
        buttons = [
            types.InlineKeyboardButton(text="Редактировать город", callback_data="city_edit"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*buttons)
        await call.message.answer("Настройки параметров поиска мероприятий", reply_markup=keyboard)

        @dp.callback_query_handler(text="city_edit")
        async def event_edit_city(call: types.CallbackQuery) -> None:
            await call.message.answer("Введите город по которому будет осуществляться поиск мероприятий ✍️!")
            await ProfilStatesGroup.city.set()

        @dp.message_handler(state=ProfilStatesGroup.city)
        async def event_city(message: types.Message, state: FSMContext):
            async with state.proxy() as data:  # Устанавливаем состояние ожидания
                data['city'] = message.text
                await message.answer(city_edit(message.from_user.id, data['city']))
            await state.finish()


@dp.callback_query_handler(text="new_notes")
async def new_notes_add(call: types.CallbackQuery) -> None:
    await call.message.answer("Напишите новую заметку ✍️!")
    await ProfilStatesGroup.text.set()  # Устанавливаем состояние


@dp.message_handler(state=ProfilStatesGroup.text)  # Принимаем состояние
async def new_notes_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:  # Устанавливаем состояние ожидания
        data['text'] = message.text
        subq = session.query(User.id).filter(User.id_tg == message.from_user.id)
        for q in subq:
            notes_new(data['text'], q.id)
    await message.answer(f'Заметка готова ✍️!')
    await state.finish()


@dp.callback_query_handler(text="my_notes")
async def new_notes_add(call: types.CallbackQuery) -> None:
    buttons = [
        types.InlineKeyboardButton(text="✍️ Редактировать", callback_data="edit_notes"),
        types.InlineKeyboardButton(text="❌ Удалить", callback_data="delete_notes"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    subq = session.query(User).filter(User.id_tg == call.from_user.id).first()
    subq_my_notes = session.query(Notes).filter(Notes.user_id == subq.id).all()
    for data in subq_my_notes:
        await call.message.answer(f'⌛️ {data.created_date.strftime("%d-%m %H:%M")}\n📝 Ваша заметка:\n'
                                  f'📋 {data.text_notes}', reply_markup=keyboard)

    @dp.callback_query_handler(text="edit_notes")
    async def edit_notes(call: types.CallbackQuery) -> None:
        sample = call.message.text
        print(sample[33:])

        await call.message.answer(f'Напишите данную заметку по новому!')
        await ProfilStatesGroup.edit.set()  # Устанавливаем состояние

        @dp.message_handler(state=ProfilStatesGroup.edit)  # Принимаем состояние
        async def edit_notes_state(message: types.Message, state: FSMContext):
            async with state.proxy() as data:  # Устанавливаем состояние ожидания
                data['edit'] = message.text
                subq = session.query(User).filter(User.id_tg == message.from_user.id).first()
                subq_notes = session.query(Notes).filter(Notes.user_id == subq.id, Notes.text_notes == sample[33:]).first()
                subq_notes.text_notes = data['edit']
                session.commit()
            await message.answer(f'Заметка изменена ✍️!')
            await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
