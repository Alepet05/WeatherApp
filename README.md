## Приложение погоды
---
>Оригинал: [видео](https://www.youtube.com/watch?v=dKxiHlZvULQ) и [веб-версия книги «Типизированный Python»](https://to.digital/typed-python/).

Программа выводит в терминал погоду по текущим GPS-координатам. Координаты берутся непосредственно с GPS-датчиков устройств под управлением Windows через пакет [winsdk](https://pypi.org/project/winsdk/).

Данные о погоде предоставляет сервис [OpenWeather](https://openweathermap.org/api).


Для запуска:
* Используйте Python версии 3.11.
* Установите зависимости командой ```pip install -r requirements.txt```.
* Впишите свой API-ключ сервиса OpenWeather в файл config.py.
* Запустите main.py.
