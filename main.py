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

        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        show = types.InlineKeyboardButton("Показать пароли")
        gen = types.InlineKeyboardButton("Нагенерировать")
        save = types.InlineKeyboardButton("Выгрузить файл с паролями")
        kb.add(gen, show, save)

        def elements(value):
            dates = []
            dates_tup = tuple(value.split(", "))
            for el in dates_tup:
                dates.append(el)
            return dates

        @bot.message_handler(commands=['start'])
        def start(message):
            bot.send_message(message.chat.id, "Бот для генерации пароля", reply_markup= kb)
            file = open(f'users/{message.from_user.username}.txt', 'w')

        @bot.message_handler(func = lambda msg: msg.text == 'Нагенерировать')
        def generate(message):
            bot.send_message(message.chat.id, "Введи название для пароля и количество символов через запятую, например: 'Название, количество'.\n"
                                              "\nНазвание вводи либо слитно, либо через нижнее подчёркивание, например: \n"
                                              "<u>'НазваниеПароля'</u> или <b>'Название_пароля'</b>", parse_mode='html')
            bot.register_next_step_handler(message, lambda msg: output(msg, ))

        def output(message):
            value = message.from_user.username
            add_res = elements(message.text)
            password = "".join(random.sample(uses, int(add_res[1])))
            out = f'Результат:\n' \
                  f'Название: {add_res[0]};\n' \
                  f'Пароль: '
            bot.send_message(message.chat.id, out)
            bot.send_message(message.chat.id, password)
            with open(f'users/{value}.txt', 'a+', encoding='utf8') as f:
                f.write(f'Название - {add_res[0]}; Пароль - {password}' + '\n')

        @bot.message_handler(func=lambda msg: msg.text == "Показать пароли")
        def show_pass(message):
            value = message.from_user.username
            read = open(f'users/{value}.txt', 'r', encoding='utf8')
            result = []
            for line in read:
                result.append(line)
            final = ''.join(str(row) for row in result)
            bot.send_message(message.chat.id, final)

        @bot.message_handler(func=lambda msg: msg.text == 'Выгрузить файл с паролями')
        def load_pass(message):
            value = message.from_user.username
            bot.send_message(message.chat.id, f'Ваши пароли находятся в этом файле: \n')
            bot.send_document(message.chat.id, document=open(f'users/{value}.txt', 'r'))

        bot.polling()

    except ValueError as e:
        with open('log.txt', 'a', encoding='UTF-8') as f:
            f.write('\n' + "ошибка: " + str(e))

    time.sleep(5)