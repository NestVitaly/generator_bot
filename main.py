import telebot
from telebot import types
import random
import time
import cowsay

while True:
    try:
        cowsay.cow('Bot Started...')
        bot = telebot.TeleBot('6083235314:AAFQIA81hSoIT8vZ91J1IdMXx0jPbeIzwKQ')

        upper_case = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        lower_case = 'qwertyuiopasdfghjklzxcvbnm'
        symbols = '!@#$%^&\/|'
        numbers = '1234567890'

        uses = upper_case + lower_case + symbols + numbers

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        gen = types.InlineKeyboardButton("Нагенерировать")
        kb.add(gen)



        def elements(value):
            dates = []
            dates_tup = tuple(value.split(" "))
            for el in dates_tup:
                dates.append(el)
            return dates


        @bot.message_handler(commands=['start'])
        def start(message):
            bot.send_message(message.chat.id, "Бот для генерации пароля", reply_markup= kb)

        @bot.message_handler(func = lambda msg: msg.text == 'Нагенерировать')
        def generate(message):
            bot.send_message(message.chat.id, "Введи название для пароля и количество символов.\n"
                                              "Название вводи либо слитно, либо через нижнее подчёркивание, например: \n"
                                              "<u>'НазваниеПароля'</u> или <u>'Название_пароля'</u>", parse_mode='html')
            bot.register_next_step_handler(message, lambda msg: output(msg, ))

        def output(message):
            value = message.text
            add_res = elements(value)
            password = "".join(random.sample(uses, int(add_res[1])))
            out = f'Результат:\n' \
                  f'Название - {add_res[0]};\n' \
                  f'Пароль - {password}'
            bot.send_message(message.chat.id, out)



        bot.polling()
    except ValueError as e:
        with open('log.txt', 'a', encoding='UTF-8') as f:
            f.write('\n' + "ошибка: " + str(e))
        f.close()

    time.sleep(5)