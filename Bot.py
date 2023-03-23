import os
import logging
import keyboard as kb
from extraction.weather import weather, weather_long
from Database import session
from dotenv import load_dotenv
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from Database import User, Notes, user_entry, notes_new, city_edit

load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv("TOKEN"))

dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


class ProfilStatesGroup(StatesGroup):
    text = State()
    city = State()
    edit = State()
    weather = State()
    weather_long = State()

@dp.message_handler(commands="start")
async def cmd_random(message: types.Message):
    """
    Стартовое приветствие пользователя с кнопками на реализованные функции
    """
    user_name = f"{message.from_user.first_name} {message.from_user.last_name}"
    user_entry(message.from_user.id, user_name, None, message.date)
    await message.answer(
        f'Привет {message.from_user.first_name}!👋 Я БОТИНОК многофункциональный!🤖 Пока во мне реализованы заметки!✍️',
        reply_markup=kb.keyboard_cmd_random)


################################ЗАМЕТКИ########################################

@dp.callback_query_handler(text="botinok_info_notes")
async def botinok_info_notes(call: types.CallbackQuery) -> None:
    """

    :param call:
    :return:
    """
    await call.message.answer("👞 БОТИНОК для заметок! 👞\n🗒 В меня вы можете записывать ваши заметки 🗒\n"
                              "❗️ Как большие, так и не очень ❗\n"
                              "🖊 Реализована возможность редактировать именно ваши заметки\n"
                              "❌ Также можете удалить любую заметку! ❌\n"
                              "⏪ Вернуться в стартовое меню /start 🔙", reply_markup=kb.keyboard_send_random_value)

@dp.callback_query_handler(text="new_notes")
async def new_notes_add(call: types.CallbackQuery) -> None:
    """

    :param call:
    :return:
    """
    await call.message.answer("Напишите новую заметку ✍️!")
    await ProfilStatesGroup.text.set()  # Устанавливаем состояние


@dp.message_handler(state=ProfilStatesGroup.text)  # Принимаем состояние
async def new_notes_add(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return:
    """
    async with state.proxy() as data:  # Устанавливаем состояние ожидания
        data['text'] = message.text
        subq = session.query(User.id).filter(User.id_tg == message.from_user.id)
        for q in subq:
            notes_new(data['text'], q.id)
    await message.answer(f'Заметка готова ✍️!')
    await state.finish()


@dp.callback_query_handler(text="my_notes")
async def new_notes_add(call: types.CallbackQuery) -> None:
    """

    :param call:
    :return:
    """
    subq = session.query(User).filter(User.id_tg == call.from_user.id).first()
    subq_my_notes = session.query(Notes).filter(Notes.user_id == subq.id).all()
    for data in subq_my_notes:
        await call.message.answer(f'⌛️ {data.created_date.strftime("%d-%m %H:%M")}\n'
                                  f'📋 {data.text_notes}', reply_markup=kb.keyboard_new_notes_add)

    @dp.callback_query_handler(text="edit_notes")
    async def edit_notes(call: types.CallbackQuery) -> None:
        """

        :param call:
        :return:
        """
        sample = call.message.text
        await call.message.answer(f'Напишите данную заметку по новому!')
        await call.answer(f'Лучше воспользуйтесь копи пастом и вставьте в чат ваши изменения!', show_alert=True)
        await ProfilStatesGroup.edit.set()  # Устанавливаем состояние

        @dp.message_handler(state=ProfilStatesGroup.edit)  # Принимаем состояние
        async def edit_notes_state(message: types.Message, state: FSMContext):
            """

            :param message:
            :param state:
            :return:
            """
            async with state.proxy() as data:  # Устанавливаем состояние ожидания
                data['edit'] = message.text
                subq = session.query(User).filter(User.id_tg == message.from_user.id).first()
                subq_notes = session.query(Notes).filter(Notes.user_id == subq.id,
                                                         Notes.text_notes == sample[33:]).first()
                subq_notes.text_notes = data['edit']
                session.commit()
            await message.answer(f'Заметка изменена ✍️!')
            await state.finish()
            # Подумать как решить проблему по редактированию

    @dp.callback_query_handler(text="delete_notes")
    async def delete_notes(call: types.CallbackQuery) -> None:
        """

        :param call:
        :return:
        """
        sample = call.message.text
        subq = session.query(User).filter(User.id_tg == call.from_user.id).first()
        subq_notes = session.query(Notes).filter(Notes.user_id == subq.id, Notes.text_notes == sample[33:]).first()
        session.delete(subq_notes)
        session.commit()
        await call.message.answer(f'Данная заметка удалена!')

#################################################################

####################МЕРОПРИЯТИЯ##################################

@dp.callback_query_handler(text="events_data")
async def events_data_info(call: types.CallbackQuery) -> None:
    """

    :param call:
    :return:
    """
    await call.message.answer("👞 Самая крутая способность БОТИНКА! 👞\n🎪 Если вы в раздумьях куда сходить? 🥊\n"
                              "❗️ Тогда вам непременно ко мне❗\n"
                              "🤖 Я подскажу куда сходить в вашем городе 🌃\n"
                              "⌚️ Даже дам информацию на ближайшие 3 дня\n"
                              "💜 Пользуйся, пока я добрый 💜\n"
                              "⏪ Вернуться в стартовое меню /start 🔙", reply_markup=kb.keyboard_event)

    @dp.callback_query_handler(text="ext_data_event")
    async def event_settings(call: types.CallbackQuery):
        """

        :param call:
        :return:
        """
        pass

    @dp.callback_query_handler(text="setting")
    async def event_settings(call: types.CallbackQuery):
        """

        :param call:
        :return:
        """
        await call.message.answer("Настройки параметров поиска мероприятий", reply_markup=kb.keyboard_event_settings)

        @dp.callback_query_handler(text="city_edit")
        async def event_edit_city(call: types.CallbackQuery) -> None:
            """

            :param call:
            :return:
            """
            await call.message.answer("Введите город по которому будет осуществляться поиск мероприятий ✍️!")
            await ProfilStatesGroup.city.set()

        @dp.message_handler(state=ProfilStatesGroup.city)
        async def event_city(message: types.Message, state: FSMContext):
            """

            :param message:
            :param state:
            :return:
            """
            async with state.proxy() as data:  # Устанавливаем состояние ожидания
                data['city'] = message.text
                await message.answer(city_edit(message.from_user.id, data['city']) + "📌")
            await state.finish()

##############################################################################

############################ПОГОДА############################################

@dp.callback_query_handler(text="weather_start")
async def weather_info(call: types.CallbackQuery) -> None:
    """

    :param call:
    :return:
    """
    await call.message.answer("🏞 ПОГОДНЫЙ БОТИНОК! 🌅\n🗺 Информирую очень подробно о погоде в вашем городе!\n"
                              "❗🌁 Вам нужно написать только свой город❗\n"
                              "⏪ Вернуться в стартовое меню /start 🔙", reply_markup=kb.keyboard_weather_long)

@dp.callback_query_handler(text="weather")
async def new_weather(call: types.CallbackQuery) -> None:
    """

    :param call:
    :return:
    """
    await call.message.answer("Привет! Напиши мне название города и я пришлю сводку погоды!")
    await ProfilStatesGroup.weather.set()

    @dp.message_handler(state=ProfilStatesGroup.weather)
    async def get_weather(message: types.Message, state: FSMContext):
        """

        :param message:
        :param state:
        :return:
        """
        async with state.proxy() as data:  # Устанавливаем состояние ожидания
            data["weather"] = message.text
            await message.reply(weather(data["weather"]))
            await state.finish()


@dp.callback_query_handler(text="weather_long")
async def new_weather(call: types.CallbackQuery) -> None:
    """

    :param call:
    :return:
    """
    await call.message.answer("Привет! Напиши мне название города и я пришлю сводку погоды на ближайшие 5 дней! Утро и вечер!")
    await ProfilStatesGroup.weather_long.set()

    @dp.message_handler(state=ProfilStatesGroup.weather_long)
    async def get_weather(message: types.Message, state: FSMContext):
        """

        :param message:
        :param state:
        :return:
        """
        async with state.proxy() as data:  # Устанавливаем состояние ожидания
            data["weather_long"] = message.text
            for i in weather_long(data["weather_long"]):
                await message.reply(i)
            await state.finish()

###

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
