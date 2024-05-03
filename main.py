'''Слой, запускающий приложение и связывающий остальные слои'''

from coordinates import get_gps_coordinates
from weather import get_weather
from weather_formatter import format_weather


def main():
    coordinates = get_gps_coordinates()
    weather = get_weather(coordinates)
    print(format_weather(weather))
