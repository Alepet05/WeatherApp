'''Слой, запускающий приложение и связывающий остальные слои'''

from coordinates import get_gps_coordinates
from weather import get_weather
from weather_formatter import format_weather
from exceptions import CantGetCoordinates, ApiServiceError


def main():
    try:
        coordinates = get_gps_coordinates()
    except CantGetCoordinates:
        print('Не смогли получить GPS-координаты')
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print('Не смогли получить погоду от API сервиса погоды')
        exit(1)
    print(format_weather(weather))


if __name__ == '__main__':
    main()
