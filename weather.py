'''Получение по координатам погоды'''

from typing import NamedTuple, Literal
from datetime import datetime
from enum import Enum
import requests
from requests.exceptions import RequestException
import json
from json import JSONDecodeError

from coordinates import Coordinates
from exceptions import ApiServiceError
import config


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
    response = _get_openweather_response(
        latitude=coordinates.latitude,
        longitude=coordinates.longitude
    )
    weather = _parse_openweather_response(response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    url = config.OPENWEATHER_URL.format(
        latitude=latitude,
        longitude=longitude
    )
    try:
        response = requests.get(url)
        return response.text
    except RequestException:
        raise ApiServiceError


def _handle_errors(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, KeyError):
            raise ApiServiceError
    return _wrapper


@_handle_errors
def _parse_openweather_response(response: str) -> Weather:
    try:
        data = json.loads(response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(data),
        weather_type=_parse_weather_type(data),
        humidity=_parse_humidity(data),
        sunrise=_parse_suntime(data, 'sunrise'),
        sunset=_parse_suntime(data, 'sunset'),
        city=_parse_city(data)
    )


@_handle_errors
def _parse_temperature(data: dict) -> Celsius:
    return round(data['main']['temp'])


@_handle_errors
def _parse_weather_type(data: dict) -> WeatherType:
    wheather_type_id = str(data['weather'][0]['id'])

    weather_types = {
        '2': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS
    }

    for _id, _weather_type in weather_types.items():
        if wheather_type_id.startswith(_id):
            return _weather_type

    raise ApiServiceError


@_handle_errors
def _parse_humidity(data: dict) -> Percent:
    return data['main']['humidity']


@_handle_errors
def _parse_suntime(data: dict, suntime: Literal['sunrise', 'sunset']) \
    -> datetime:
    return datetime.fromtimestamp(data['sys'][suntime])


@_handle_errors
def _parse_city(data: dict) -> str:
    return data['name']



if __name__ == '__main__':
    weather = get_weather(Coordinates(latitude=10, longitude=20))
    print(weather)
