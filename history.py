from abc import ABC, abstractmethod
from datetime import datetime
import json
import os
from typing import TypedDict
import sqlite3 as sq

from weather_formatter import format_weather
from weather import Weather
from exceptions import WeatherStorageError


class HistoryRecord(TypedDict):
    date: str
    weather: str


class WeatherStorage(ABC):
    '''Абстрактный класс любого хранилища погоды'''

    @abstractmethod
    def save(self, weather: Weather):
        pass

    @staticmethod
    def _handle_error(func):
        def _wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except OSError:
                raise WeatherStorageError
            except sq.Error:
                raise WeatherStorageError
        return _wrapper


class TextFileWeatherStorage(WeatherStorage):
    '''Сохраняет погоду в txt файле'''
    def __init__(self, file: str):
        self._file = file

    @WeatherStorage._handle_error
    def save(self, weather: Weather):
        now = datetime.now()
        formatted_weather = format_weather(weather)

        with open(self._file, 'a', encoding='utf-8') as f:
            f.write(f'\n{now}\n{formatted_weather}\n')


class JsonFileWeatherStorage(WeatherStorage):
    '''Сохраняет погоду в JSON файл'''
    def __init__(self, file: str):
        self._file = file
        self._init_storage()

    def save(self, weather: Weather):
        history = self._read_history()

        history.append(HistoryRecord(
            date=str(datetime.now()),
            weather=format_weather(weather)
        ))

        self._write(history)

    @WeatherStorage._handle_error
    def _init_storage(self):
        if not os.path.exists(self._file):
            with open(self._file, 'w', encoding='utf-8') as f:
                f.write('[]')

    @WeatherStorage._handle_error
    def _read_history(self) -> list[HistoryRecord]:
        with open(self._file, encoding='utf-8') as f:
            return json.load(f)

    @WeatherStorage._handle_error
    def _write(self, history: list[HistoryRecord]):
        with open(self._file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)


class DatabaseWeatherStorage(WeatherStorage):
    '''Сохраняет погоду в базу данных SQLite'''
    def __init__(self, _file: str):
        self.con = sq.connect(_file)
        self.cur = self.con.cursor()
        self._create_table()

    @WeatherStorage._handle_error
    def save(self, weather: Weather):
        with self.con:
            now = datetime.now()
            self.cur.execute('''INSERT INTO weather (date, temperature, weather_type,
                                                    humidity, sunrise, sunset, city)
                                VALUES(?, ?, ?, ?, ?, ?, ?)''', (now, *weather))
            self.con.commit()

        self._close()

    @WeatherStorage._handle_error
    def _create_table(self):
        with self.con:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS weather(
                            weather_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                            date                DATETIME,
                            temperature         INTEGER,
                            weather_type        VARCHAR(20),
                            humidity            INTEGER,
                            sunrise             DATETIME,
                            sunset              DATETIME,
                            city                VARCHAR(50)
            )''')

    def _close(self):
        self.con.close()

def save_weather(weather: Weather, storage: WeatherStorage):
    '''Сохраняет погоду в хранилище'''
    storage.save(weather)
