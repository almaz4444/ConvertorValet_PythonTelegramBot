import requests
import telebot
import telebot.types as types

from data import *


# Словарь из chat.id
# Чтобы у каждого могло конвертироваться индивидуально {id: (inValute, toValute)}
chats = {}

# Клавиатуры
keyboardValute = types.InlineKeyboardMarkup(row_width=7)  # Коды валют
keyboardBack = types.InlineKeyboardMarkup()               # Кнопка "Назад"
keyboardMain = types.InlineKeyboardMarkup()               # Главная "страница"

old_message = None

bot = telebot.TeleBot(TOKEN)


def init_keyboards():
    """Инициализация клавиатур (добавление кнопок в клавиатуры)"""

    keyboardValute.add(
        types.InlineKeyboardButton(
            "🔙 Назад", callback_data="back"
        )
    )
    keyboardBack.add(
        types.InlineKeyboardButton(
            "🔙 Назад", callback_data="back"
        )
    )
    keyboardMain.add(
        types.InlineKeyboardButton(
            "🔁 Конвертировать 🔁", callback_data="convert"
        )
    )
    keyboardMain.add(
        types.InlineKeyboardButton(
            "ℹ️ О проекте ℹ️", callback_data="info"
        )
    )

    # Добавление кнопок с кодами валют
    # (сделано данным образом, для того, чтобы кнопки могли выстраиваться в ряд)
    keyboardButtons = []
    for valuteCode in get_valutes_names().keys():
        keyboardButtons.append(
            types.InlineKeyboardButton(
                valuteCode, callback_data=valuteCode
            )
        )
    keyboardValute.add(*keyboardButtons)


def get_valutes_courses():
    """Возвращает словарь с кодами валют и их курсом в рублях {код: курс}"""

    valutes = requests.get(URL_VALUTES).json()["Valute"]
    valutesDict = {"RUB": 1}    # Курса рубля нет на сайте (удивительно...)

    for valute in valutes:
        valutesDict[valute] = int(valutes[valute]["Value"]) / \
            int(valutes[valute]["Nominal"])
    return dict(sorted(valutesDict.items()))


def get_time():
    """Возвращает дату и время актуального курса валют <ГГ.ММ.ДД ЧЧ.ММ.СС>"""

    date = requests.get(URL_VALUTES).json()['Date']
    return f"{date.replace('T', ' ').split('+')[0]} по МСК"


def get_valutes_names():
    """Возвращает словарь с кодами и названиями валют (некоторые валюты в род. падеже) {код: название}"""

    valutes = requests.get(URL_VALUTES).json()["Valute"]
    valutesDict = {"RUB": "Российский рубль"}

    for valute in valutes:
        valutesDict[valute] = valutes[valute]["Name"]
    return valutesDict


def formatNumber(num: float):
    """
    Если в числа присутствует .0, то возвращает чило без него, иначе вернёт исходное число:
    formatNumber(10.0) => 10
    formatNumber(10.5) => 10.5
    """
    if round(num) - num == 0:
        return round(num)
    else:
        return num


def is_digit(num_string: str):
    """
    Возвращает True, если аргумент является числом (int, float)
    иначе - False
    """
    try:
        float(num_string)
        return True
    except ValueError:
        return False


@bot.message_handler(commands=['start'])  # При команде /start
def start_message(message):
    """Отправим стартовое сообщение"""

    bot.send_message(message.chat.id,
                     start_message_text,
                     reply_markup=keyboardMain
                     )


# При нажатии на любую кнопку
@bot.callback_query_handler(func=lambda call: True)
def receivedKey(call):
    if call.message:  # Если сообщение не пустое
        inValute, toValute = chats.setdefault(
            str(call.message.chat.id), ("", ""))
        text, board = None, None

        if call.data == "info":
            text = bot_info_text
            board = keyboardBack
        elif call.data == "convert":
            text = "Выбери код валюты для перевода:"
            board = keyboardValute
        elif call.data == "back":
            text = "Те та валюта? Тогда выбери другую:"
            if toValute:                # Если введдена валюта, в которую перевести
                toValute = ""
                board = keyboardValute
            elif inValute:              # Иначе если введдена валюта, из которой перевести
                inValute = ""
                board = keyboardValute
            else:
                text = start_message_text
                board = keyboardMain
        elif not (inValute and toValute):       # Если не введена любая валюта для перевода
            if call.data in get_valutes_courses():  # Если код валюты есть в списке (на всякий случай)
                if not inValute:   # Если не введдена валюта, из которой перевести
                    text = "Отлично! Выбери код валюты в которую надо перевести."
                    board = keyboardValute
                    inValute = call.data
                elif not toValute:  # Иначе если не введдена валюта, в которую перевести
                    text = "Хорошо, теперь напиши мне сумму для перевода."
                    board = keyboardBack
                    toValute = call.data

        chats[str(call.message.chat.id)] = (inValute, toValute)

        # Меняем сообщение сообщение
        global old_message
        old_message = bot.edit_message_text(text, call.message.chat.id,
                                            call.message.id, reply_markup=board
                                            ).message_id


@ bot.message_handler(content_types='text')  # Если сообщение текстовое
def receivedSumValute(message):
    inValute, toValute = chats.setdefault(str(message.chat.id), ("", ""))

    if (inValute and toValute):  # Если введены обе валюты для перевода
        text, board = None, None

        if is_digit(message.text):  # Если это число (float или int)
            valutesCourses = get_valutes_courses()
            valutesName = get_valutes_names()
            inValuteCourse = valutesCourses[inValute]
            toValuteCourse = valutesCourses[toValute]

            # Рассчитываем сконвертированную сумму:
            course = inValuteCourse / toValuteCourse
            sumValute = round(float(message.text) * course, 2)

            inValuteSum = '{0:,}'.format(
                formatNumber(float(message.text))
            ).replace(',', ' ')
            toValuteSum = '{0:,}'.format(
                formatNumber(sumValute)
            ).replace(',', ' ')

            text = f"Готово!\nНа данный момент ({get_time()}) 🕑\n \
                    {inValuteSum} {valutesName[inValute]} ({inValute}) - примерно {toValuteSum} {valutesName[toValute]} ({toValute}).\n \
                    Курс конвертации: {round(course, 2)} {inValute}/{toValute}\n \
                    Обращайся ещё, буду рад помочь! :)"
            board = keyboardMain
            inValute, toValute = "", ""
        else:
            text = "Упс! Пожоже это не число :(\nНапиши сумму ещё раз."
            board = None  # Не заменяем клавиатуру

        chats[str(message.chat.id)] = (inValute, toValute)

        # Удаляем сообщение пользователя
        bot.delete_message(message.chat.id, message.id)

        # Меняем сообщение сообщение
        bot.edit_message_text(text, message.chat.id,
                              old_message, reply_markup=board
                              )


if (__name__ == "__main__"):
    init_keyboards()
    bot.infinity_polling()
