Telegram-бот конвертер валют
========

Ведение
------------
Telegram-bot для конвертации валют

Бот написан с использованием следуйщих библиотек:
* [Telebot](https://pypi.org/project/pyTelegramBotAPI/)
* [Requests](https://pypi.org/project/requests/)
* [Dotenv](https://pypi.org/project/python-dotenv/)

Конвертер валют на питоне в формате telegram-бота

Загрузка
------------
1. Создать бота в [BotFather](https://telegram.me/BotFather) и получить токен
2. Переименовать файл ``.env.dist`` в ``.env``
3. Вставить токен в `TOKEN`
3. Загрузить репозиторий

Как скачать на Windows?
```
git clone https://github.com/almaz4444/ConvertorValet_PythonTelegramBot
cd ConvertorValet_PythonTelegramBot
pip install -r requirements.txt
```

Как запустить?
```
python3 main.py
```

Технологии
--------------
* Python
* Telebot
* Requests
* Dotenv
* API

Как работает
--------------
1. Получает команду от пользователя
2. Получает курс валют в рублях от [ЦБ РФ](https://www.cbr-xml-daily.ru/)
3. Находит коэффициент умножения для получения другой валюты 
4. Отправляет пользователю сконвертированную валюту 

Скриншоты
--------------

Главный экран:

!["Ошибка загрузки"](/Screenhots/Main.png)

Конвертация валюты:

!["Ошибка загрузки"](/Screenhots/ConvertValet.png)

Ответ бота:

!["Ошибка загрузки"](/Screenhots/Output.png)