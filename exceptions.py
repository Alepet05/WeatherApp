class CantGetCoordinates(Exception):
    '''Не можем получить текуще GPS координаты'''
    pass


class ApiServiceError(Exception):
    '''Не удалось установить соединение'''
    pass
