import os

from dotenv import load_dotenv


load_dotenv()

# URL для парсинга текущих курсов валют в рублях
URL_VALUTES = "https://www.cbr-xml-daily.ru/daily_json.js"
TOKEN: str = os.getenv('TOKEN')  # type: ignore

start_message_text = '''
Привет!
Хочешь сконвертировать валюту?
Я могу тебе с этим помочь :)
'''

bot_info_text = '''
Если хочешь сконвертировать валюту, то обращайся ко мне :)
Для этого выбери валюту из которой и в которую перевести, а после напиши сумму 🆗
Меня сделал Сальманов Алмаз Русланович 👨‍💻
А вот мой исходный код 😱: https://github.com/almaz4444/ConvertorValet_PythonTelegramBot
'''
