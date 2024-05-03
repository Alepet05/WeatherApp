'''Форматирование погоды для печати'''

from weather import Weather


def format_weather(weather: Weather):
    '''Форматирует данные о погоде в строку'''
    return (
        f'{weather.city}, температура: {weather.temperature}°C, '
        f'{weather.weather_type.value}\n'
        f'Влажность: {weather.humidity}%\n'
        f'Восход: {weather.sunrise.strftime("%H:%M")}\n'
        f'Закат: {weather.sunset.strftime("%H:%M")}'
    )


if __name__ == '__main__':
    from datetime import datetime
    from weather import WeatherType
    print(format_weather(Weather(
        temperature=25,
        weather_type=WeatherType.CLEAR,
        humidity=53,
        sunrise=datetime.fromisoformat("2022-05-03 04:00:00"),
        sunset=datetime.fromisoformat("2022-05-03 20:25:00"),
        city="Москва"
    )))
