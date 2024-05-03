'''Получение текущих координат'''

from typing import NamedTuple


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_gps_coordinates() -> Coordinates:
    '''Возвращает текущие координаты используя GPS_датчик в ноутбуке'''
    return Coordinates(latitude=0, longitude=0)


if __name__ == '__main__':
    coordinates = get_gps_coordinates()
    print(coordinates.latitude)
    print(coordinates.longitude)

