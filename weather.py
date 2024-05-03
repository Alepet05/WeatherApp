'''Получение по координатам погоды'''

from typing import NamedTuple
from datetime import datetime
from enum import Enum

from coordinates import Coordinates


Celsius = int
Percent = int


class WeatherType(str, Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    humidity: Percent
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    '''Возвращает данные о погоде через API OpenWeather'''
    return Weather(
        temperature=10,
        weather_type=WeatherType.CLEAR,
        humidity=60,
        sunrise=datetime.fromisoformat('2024-05-03 04:00:00'),
        sunset=datetime.fromisoformat('2024-05-03 21:00:00'),
        city='Москва'
    )


if __name__ == '__main__':
    weather = get_weather(Coordinates(latitude=10, longitude=20))
    print(weather.temperature, weather.weather_type)
