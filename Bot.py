import datetime
import os
import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import keyboard as kb
from extraction.weather import weather, weather_long
from Database import session
from dotenv import load_dotenv
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from Database import User, Notes, user_entry, notes_new, city_edit, conclusion_event, return_city, rerurn_alp_cuty

load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv("TOKEN"))

dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

alphabet_all = rerurn_alp_cuty()

class ProfilStatesGroup(StatesGroup):
    text = State()
    city = State()
    edit = State()
    weather = State()
    weather_long = State()


def gen_markup(quanity: int, prefix: str, row_width: int) -> InlineKeyboardMarkup:
    gen_markup_key = []
    markup = InlineKeyboardMarkup(row_width=row_width)
    for keys_alph in alphabet_all:
        gen_markup_key.append(keys_alph)
    for i in range(quanity):
        markup.insert(InlineKeyboardButton(f"{gen_markup_key[i]}", callback_data=f"{prefix}:{gen_markup_key[i]}"))
    return markup


@dp.message_handler(commands="test")
async def cmd_random(message: types.Message):
    markup = gen_markup(len(alphabet_all), "prefix", 5)
    await message.answer(
        f'Привет {message.from_user.first_name}!👋 Я БОТИНОК многофункциональный!🤖 Пока во мне реализованы заметки!✍️',
        reply_markup=markup)


    # @dp.callback_query_handler(text=f"prefix:{}")
    # async def returnstart(call: types.CallbackQuery) -> None:
    #     pass


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


@dp.callback_query_handler(text="returnstart")
async def returnstart(call: types.CallbackQuery) -> None:
    """
    Стартовое приветствие пользователя на реализованные функции в виде inline кнопок
    """
    await call.message.answer(
        f'Привет {call.from_user.first_name}!👋 Я БОТИНОК многофункциональный!🤖 Пока во мне реализованы заметки!✍️',
        reply_markup=kb.keyboard_cmd_random)


################################ЗАМЕТКИ########################################

@dp.callback_query_handler(text="botinok_info_notes")
async def botinok_info_notes(call: types.CallbackQuery) -> None:
    """
    Основная функция для заметок, с информацией о реализации
    :return: inline кнопки 'Новая заметка' и 'Мои заметки'
    """
    await call.message.answer("👞 БОТИНОК для заметок! 👞\n🗒 В меня вы можете записывать ваши заметки 🗒\n"
                              "❗️ Как большие, так и не очень ❗\n"
                              "🖊 Реализована возможность редактировать именно ваши заметки\n"
                              "❌ Также можете удалить любую заметку! ❌\n"
                              "⏪ Вернуться в стартовое меню /start 🔙", reply_markup=kb.keyboard_send_random_value)


@dp.callback_query_handler(text="new_notes")
async def new_notes_add(call: types.CallbackQuery) -> None:
    """
    Создание новой заметки с помощью машины состояний
    """
    await call.message.answer("Напишите новую заметку ✍️!")
    await ProfilStatesGroup.text.set()  # Устанавливаем состояние


@dp.message_handler(state=ProfilStatesGroup.text)  # Принимаем состояние
async def new_notes_add(message: types.Message, state: FSMContext):
    """
    Принимает от пользователя заметку и добавляет в БД
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
    Выдача всех заметок пользователя, фильтрация через id_tg
    """
    subq = session.query(User).filter(User.id_tg == call.from_user.id).first()
    subq_my_notes = session.query(Notes).filter(Notes.user_id == subq.id).all()
    for data in subq_my_notes:
        await call.message.answer(f'⌛️ {data.created_date.strftime("%d-%m %H:%M")}\n'
                                  f'📋 {data.text_notes}', reply_markup=kb.keyboard_new_notes_add)

    @dp.callback_query_handler(text="edit_notes")
    async def edit_notes(call: types.CallbackQuery) -> None:
        """
        Редактирование заметки
        """
        sample = call.message.text
        await call.message.answer(f'Напишите данную заметку по новому!')
        await call.answer(f'Лучше воспользуйтесь копи пастом и вставьте в чат ваши изменения!', show_alert=True)
        await ProfilStatesGroup.edit.set()  # Устанавливаем состояние

        @dp.message_handler(state=ProfilStatesGroup.edit)  # Принимаем состояние
        async def edit_notes_state(message: types.Message, state: FSMContext):
            """
            Машинное состояние принимает от пользователя новую измененную заметку
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

    @dp.callback_query_handler(text="delete_notes")
    async def delete_notes(call: types.CallbackQuery) -> None:
        """
        Удаление заметки из БД
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
    await call.message.answer("👞 Список культурно-массовых мероприятий на 3 дня ", reply_markup=kb.keyboard_event)

    @dp.callback_query_handler(text="ext_data_event")
    async def event_settings(call: types.CallbackQuery):
        buttons_finish = [types.InlineKeyboardButton(text="🔙Назад", callback_data="events_data")]
        keyboard_finish = types.InlineKeyboardMarkup(row_width=1)
        keyboard_finish.add(*buttons_finish)
        buttons_set = [types.InlineKeyboardButton(text="⚙️ Настройки", callback_data="setting")]
        keyboard_set = types.InlineKeyboardMarkup(row_width=1)
        keyboard_set.add(*buttons_set)
        try:
            events_for_user = conclusion_event(call.from_user.id)
            count_event = 0
            for pars_event in events_for_user:
                buttons_afisha = [types.InlineKeyboardButton(text="🔗Страница мероприятия", url=f"{pars_event[4]}")]
                keyboard_afisha = types.InlineKeyboardMarkup(row_width=1)
                keyboard_afisha.add(*buttons_afisha)

                try:
                    await call.message.answer_photo(pars_event[3], caption=
                    f"🗓Дата проведения мероприятия - {pars_event[0]}\n"
                    f"🎵Жанр - {pars_event[1]}\n"
                    f"☑️Название - {pars_event[2]}\n", reply_markup=keyboard_afisha)
                    count_event += 1

                except:
                    with open("save_error.txt", "a") as open_file_error:
                        open_file_error.write(f"{datetime.datetime.now()}.  "
                                              f"Пользователь - {call.from_user.id}.  "
                                              f"Ошибка - {pars_event[3]}.  "
                                              f"Ссылка - {pars_event[4]}\n")

            await call.message.answer(
                f"Вывод завершен. Мероприятий в {return_city(call.from_user.id)[0]} - {count_event}",
                reply_markup=keyboard_finish)
        except:
            await call.message.answer(f"Невозможно отобразить информацию по проводимым мероприятиям. "
                                      f"Возможно у Вас не установлен город. Зайдите в меню настроек.",
                                      reply_markup=keyboard_set)

    @dp.callback_query_handler(text="setting")
    async def event_settings(call: types.CallbackQuery):

        try:
            set_city = return_city(call.from_user.id)[0]
        except TypeError:
            set_city = "❗❗❗ ГОРОД НЕ УСТАНОВЛЕН ❗❗❗"

        await call.message.answer("🏛️Меню настройки поиска и отображения мероприятий проводимых в Вашем городе.\n\n"
                                  "Текущие настройки:\n"
                                  f"🏙город - {set_city}",
                                  reply_markup=kb.keyboard_event_settings)

        @dp.callback_query_handler(text="city_edit")
        async def event_edit_city(call: types.CallbackQuery) -> None:
            await call.message.answer("Введите город по которому будет осуществляться поиск мероприятий ✍️!")
            await ProfilStatesGroup.city.set()

        @dp.message_handler(state=ProfilStatesGroup.city)
        async def event_city(message: types.Message, state: FSMContext):
            async with state.proxy() as data:  # Устанавливаем состояние ожидания
                data['city'] = message.text
                # await message.answer(city_edit(message.from_user.id, data['city']) + "📌")
                if city_edit(message.from_user.id, data['city']) == "Данный город отсутствует в базе":
                    await message.answer(city_edit(message.from_user.id, data['city']),
                                         reply_markup=kb.keyboard_event_settings)
                else:
                    await message.answer(city_edit(message.from_user.id, data['city']) + "📌",
                                         reply_markup=kb.keyboard_event)
            await state.finish()


##############################################################################

############################ПОГОДА############################################

@dp.callback_query_handler(text="weather_start")
async def weather_info(call: types.CallbackQuery) -> None:
    """
    Основная погодная функция с инофрмацией
    return: inline кнопки 'Погода сейчас' и 'На 5 дней'
    """
    await call.message.answer("🏞 ПОГОДНЫЙ БОТИНОК! 🌅\n🗺 Информирую очень подробно о погоде в вашем городе!\n"
                              "❗🌁 Вам нужно написать только свой город❗\n"
                              "⏪ Вернуться в стартовое меню /start 🔙", reply_markup=kb.keyboard_weather_long)


@dp.callback_query_handler(text="weather")
async def new_weather(call: types.CallbackQuery) -> None:
    """
    Выдает погоду сейчас по городу пользователя. Реализация if: если город пользователя имеется в БД и
    else: если нету, город еще не добавлен в БД
    Имеется функция weather импортирована из extraction.weather.py
    """
    ext_city_db = session.query(User).filter(User.id_tg == call.from_user.id).first()
    if ext_city_db.city:
        await call.message.answer(
            "Выдаю сводку погоды сейчас в твоем городе! Но есть возможность выбрать другой город.",
            reply_markup=kb.keyboard_weather_another)
        await call.message.answer(weather(return_city(call.from_user.id)[0]))

    else:
        await call.message.answer("Напиши мне название города!")
        await ProfilStatesGroup.weather.set()

        @dp.message_handler(state=ProfilStatesGroup.weather)
        async def get_weather(message: types.Message, state: FSMContext):
            """
            Машинное состояние принимает город от польхователя и выполняет функцию weather
            """
            async with state.proxy() as data:  # Устанавливаем состояние ожидания
                data["weather"] = message.text
                await message.answer(weather(data["weather"]))
                await state.finish()

    @dp.callback_query_handler(text="weather_city")
    async def new_weather(call: types.CallbackQuery) -> None:
        """
        Выдача погоды пользователю по введенному в чат городу
        """
        await call.message.answer("Напиши мне название города!")
        await ProfilStatesGroup.weather.set()

        @dp.message_handler(state=ProfilStatesGroup.weather)
        async def get_weather(message: types.Message, state: FSMContext):
            """
            Машинное состояние принимает город от пользователя и weather выдает погоду
            """
            async with state.proxy() as data:  # Устанавливаем состояние ожидания
                data["weather"] = message.text
                await message.answer(weather(data["weather"]))
                await state.finish()


@dp.callback_query_handler(text="weather_long")
async def new_weather(call: types.CallbackQuery) -> None:
    """
    Выдача погоды на ближайшие 5 дней. Утро и вечер
    Реализия if: если имеется город пользователя в БД, else: если города нету
    Встроенная функция погоды weather_long из extraction.weather.py
    """
    ext_city_db = session.query(User).filter(User.id_tg == call.from_user.id).first()
    if ext_city_db.city:
        buttons_weather_another_long = [
            types.InlineKeyboardButton(text=f'🗽 {ext_city_db.city}', callback_data="weather_my_city"),
            types.InlineKeyboardButton(text="🏙 Другой город", callback_data="weather_city_settings"),
            types.InlineKeyboardButton(text="🔙 В начало", callback_data="returnstart")
        ]
        keyboard_weather_another_long = types.InlineKeyboardMarkup(row_width=2)
        keyboard_weather_another_long.add(*buttons_weather_another_long)
        await call.message.answer(
            "Привет! Сводка погоды на ближайшие 5 дней! Утро и вечер! Выбери конфигурацию!",
            reply_markup=keyboard_weather_another_long)

        @dp.callback_query_handler(text="weather_my_city")
        async def weather_my_city(call: types.CallbackQuery) -> None:
            """
            Выдача погоды на ближайшие 5 дней функцией weather_long
            """
            if weather_long(ext_city_db.city) == "Проверьте название города":
                await call.message.answer(weather_long(ext_city_db.city))
            else:
                for i in weather_long(ext_city_db.city):
                    await call.message.answer(i)

        @dp.callback_query_handler(text="weather_city_settings")
        async def weather_city_settings(call: types.CallbackQuery) -> None:
            """
            Машинное состояние принимает город от пользователя из чата
            """
            await call.message.answer(
                'Напиши мне название города и я пришлю сводку погоды на ближайшие 5 дней! Утро и вечер!')
            await ProfilStatesGroup.weather_long.set()

            @dp.message_handler(state=ProfilStatesGroup.weather_long)
            async def get_weather(message: types.Message, state: FSMContext):
                """
                Берет город из машинного состояния и реализует функцию weather_long,
                выдает пользователю погоду на 5 дней
                """
                async with state.proxy() as data:  # Устанавливаем состояние ожидания
                    data["weather_long"] = message.text
                    if weather_long(data["weather_long"]) == "Проверьте название города":
                        await message.answer(weather_long(data["weather_long"]))
                    else:
                        for i in weather_long(data["weather_long"]):
                            await message.answer(i)
                    await state.finish()

    else:
        await call.message.answer(
            'Напиши мне название города и я пришлю сводку погоды на ближайшие 5 дней! Утро и вечер!')

        await ProfilStatesGroup.weather_long.set()

        @dp.message_handler(state=ProfilStatesGroup.weather_long)
        async def get_weather_from_user(message: types.Message, state: FSMContext):
            """
            Принимает из машинного состояния город пользователя
            Через weather_long реализует выдачу погоды на ближайшие 5 дней
            """
            async with state.proxy() as data:  # Устанавливаем состояние ожидания
                data["weather_long"] = message.text
                if weather_long(data["weather_long"]) == "Проверьте название города":
                    await message.answer(weather_long(data["weather_long"]))
                else:
                    for i in weather_long(data["weather_long"]):
                        await message.answer(i)
                await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
