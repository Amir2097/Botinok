from dotenv import load_dotenv
import os
import logging
from aiogram import Bot, Dispatcher, types, executor



load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv("TOKEN"))

dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["👾 БОТИНОК для заметок 👾"]
    # buttons = ["Новая заметка", "Мои заметки", "Редактирование", "БОТИНОК", "Удаление", "Напоминание"]
    keyboard.add(*buttons)
    await message.answer("Привет!👋 Я БОТИНОК многофункциональный!🤖 Пока во мне реализованы заметки!✍️", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "🤖 БОТИНОК для заметок 🤖")
async def without_puree(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["📋 Новая заметка", "💼 Мои заметки", "✍️ Редактирование", "👞 БОТИНОК", "❌ Удаление", "✅ Напоминание"]
    keyboard.add(*buttons)

    await message.answer("БОТИНОК для ваших заметок.👞 Всегда под рукой!🤝"
                         "В меня вы можете записать все что угодно!🕵️‍♂️🧠", reply_markup=keyboard)

@dp.message_handler(commands="special_buttons")
async def cmd_special_buttons(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))
    keyboard.add(types.KeyboardButton(text="Запросить контакт", request_contact=True))
    keyboard.add(types.KeyboardButton(text="Создать викторину",
                                      request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    await message.answer("Выберите действие:", reply_markup=keyboard)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



