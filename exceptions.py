class CantGetCoordinates(Exception):
    '''Не смогли получить текущие GPS координаты'''
    pass


class ApiServiceError(Exception):
    '''Не смогли получить погоду от API сервиса погоды'''
    pass


class WeatherStorageError(Exception):
    '''Не смогли сохранить погоду в хранилище'''
    pass
