import requests
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

def weather_long(city):
    """
    :return:
    """
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={os.getenv("open_weather_token")}&units=metric&lang=ru'
        )
        data = response.json()
        new_list = []
        for key in data['list']:
            if key['dt_txt'][11:13] == '06':
                new_list.append(f"⌛️ Утром {key['dt_txt']} ⏳\n"
                        f"🌈 Погода в городе: {city}\n🌡 Температура: {key['main']['temp']}C°\n"
                        f"💦 Влажность: {key['main']['humidity']}%\n🎚 Давление: {key['main']['pressure']} мм.рт.ст.\n🌪 Ветер: {key['wind']['speed']}\n"
                        f"💥 Прекрасного ⭐️"
                        )
            elif key['dt_txt'][11:13] == '21':
                new_list.append(f"⌛️ Вечером {key['dt_txt']} ⏳\n"
                        f"🌈 Погода в городе: {city}\n🌡 Температура: {key['main']['temp']}C°\n"
                        f"💦 Влажность: {key['main']['humidity']}%\n🎚 Давление: {key['main']['pressure']} мм.рт.ст.\n🌪 Ветер: {key['wind']['speed']}\n"
                        f"💥 Прекрасного ⭐️"
                        )
        return new_list

    except Exception as ex:
        return ("Проверьте название города")


def weather(data):
    """
    :return:
    """
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={data}&appid={os.getenv("open_weather_token")}&units=metric'
        )
        data = response.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        return (f"⌛️ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ⏳\n"
                f"🌈 Погода в городе: {city}\n🌡 Температура: {cur_weather}C°\n"
                f"💦 Влажность: {humidity}%\n🎚 Давление: {pressure} мм.рт.ст.\n🌪 Ветер: {wind}\n"
                f"🌅 Восход солнца: {sunrise_timestamp.strftime('%d-%m %H:%M')}\n🌄 Закат солнца: {sunset_timestamp.strftime('%d-%m %H:%M')}\n"
                f"🕰 Продолжительность дня: {str(length_of_the_day)[:-3]}\n"
                f"💥 Прекрасного дня ⭐️"
                )

    except Exception as ex:
        return ("Проверьте название города")

# print(weather_long('Челябинск'))