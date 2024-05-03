'''Получение текущих координат'''

from typing import NamedTuple
import asyncio
import winsdk.windows.devices.geolocation as wdg
from winsdk.windows.devices.geolocation import Geoposition

from exceptions import CantGetCoordinates
import config


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_gps_coordinates() -> Coordinates:
    '''Возвращает текущие координаты используя GPS_датчик в ноутбуке'''
    coordinates = _get_winsdk_coordinates()
    return _round_coordinates(coordinates)


async def _get_winsdk_geoposition() -> Geoposition:
    locator = wdg.Geolocator()
    geoposition = await locator.get_geoposition_async()

    if geoposition.coordinate is None:
        raise CantGetCoordinates

    return geoposition


def _get_winsdk_coordinates() -> Coordinates:
    try:
        geoposition = asyncio.run(_get_winsdk_geoposition())
    except PermissionError:
        raise CantGetCoordinates
    return Coordinates(
            latitude=geoposition.coordinate.latitude, # type: ignore
            longitude=geoposition.coordinate.longitude # type: ignore
        )


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    else:
        return Coordinates(*map(
            lambda coord: round(coord, 1),
            coordinates)
        )


if __name__ == '__main__':
    coordinates = get_gps_coordinates()
    print([coordinates.latitude, coordinates.longitude])
