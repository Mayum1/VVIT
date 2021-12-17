import telebot
from telebot import types
import psycopg2
from datetime import datetime, date

token = "bot_token"
bot = telebot.TeleBot(token)

conn = psycopg2.connect(database="bot_timetable",
                        user="postgres",
                        password="123456",
                        host="localhost",
                        port="5432")


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница")
    keyboard.row("Текущая неделя", "Следующая неделя")
    bot.send_message(message.chat.id, 'Добрый день, это бот-расписание. Я могу показать Вам расписание на эту или '
                                      'следующую неделю. \n Для подробностей, пожалуйста, напишите команду /help',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Здравствуйте! Вы можете управлять этим ботом с помощью кнопок или команд,'
                                      'представленных ниже. \n \n'
                                      '**********Кнопки********** \n'
                                      'Кнопки "Понедельник", "Вторник", "Среда", "Четверг", "Пятница" позволяют вывести'
                                      ' расписание на соответствующий кнопке день текущей недели. \n'
                                      'Кнопки "Текущая неделя" и "Следующая неделя" выводят расписание на всю '
                                      'соответствующую неделю. \n \n'
                                      '**********Команды********** \n'
                                      '/week - выводит какая сейчас неделя (верхняя или нижняя). \n'
                                      '/mtuci - выводит ссылку на официальный сайт МТУСИ. \n'
                                      '/help - выводит данное сообщение.')


@bot.message_handler(commands=['mtuci'])
def mtuci_message(message):
    bot.send_message(message.chat.id, 'Официальный сайт МТУСИ – https://mtuci.ru/')


@bot.message_handler(commands=['week'])
def week_message(message):
    dateStart = date(2021, 8, 30)
    dateCurr = date(int(datetime.now().strftime('%Y')), int(datetime.now().strftime('%m')),
                int(datetime.now().strftime('%d')))
    weekCurr = (int((dateCurr - dateStart).days) // 7 + 1) % 2
    if weekCurr == 1:
        bot.send_message(message.chat.id, 'Сейчас верхняя неделя.')
    else:
        bot.send_message(message.chat.id, 'Сейчас нижняя неделя.')


@bot.message_handler(content_types=['text'])
def answer(message):
    dateStart = date(2021, 8, 30)
    dateCurr = date(int(datetime.now().strftime('%Y')), int(datetime.now().strftime('%m')),
                int(datetime.now().strftime('%d')))
    weekCurr = (int((dateCurr - dateStart).days) // 7 + 1) % 2

    cursor = conn.cursor()
    if message.text.capitalize() in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']:
        cursor.execute("SELECT * FROM timetable WHERE day=%s AND (week=%s OR week='2') ORDER BY start_time;",
                       (str(message.text.capitalize()), str(weekCurr)))
        records = list(cursor.fetchall())
        if len(records) == 0:
            timetableDay = str(message.text.capitalize()) + '\n_______________\nВ этот день пар нет.'
        else:
            timetableDay = records[0][1] + '\n_______________\n'
            for i in range(len(records)):
                timetableDay += str(i+1) + '. '
                cursor.execute("SELECT full_name FROM teacher WHERE subject=%s", [str(records[i][2])])
                teacher = str(cursor.fetchall()[0][0])
                for j in range(2, 5):
                    timetableDay += records[i][j] + ' | '
                timetableDay += teacher + '\n'
        bot.send_message(message.chat.id, timetableDay)

    if message.text.capitalize() in ['Текущая неделя', 'Следующая неделя']:
        if message.text.capitalize() == 'Следующая неделя':
            weekCurr = abs(weekCurr - 1)
        cursor.execute("SELECT * FROM timetable WHERE week=%s OR week=2", [str(weekCurr)])
        records = list(cursor.fetchall())
        timetableDay = 'Понедельник\n_______________\n'
        day = records[0][1]
        n = 1
        for i in range(len(records)):
            if records[i][1] != day:
                timetableDay += '\n' + records[i][1] + '\n_______________\n'
                day = records[i][1]
                n = 1
            timetableDay += str(n) + '. '
            cursor.execute("SELECT full_name FROM teacher WHERE subject=%s", [str(records[i][2])])
            teacher = str(cursor.fetchall()[0][0])
            for j in range(2, 5):
                timetableDay += records[i][j] + ' | '
            timetableDay += teacher + '\n'
            n += 1
        bot.send_message(message.chat.id, timetableDay)

    if message.text.lower() not in ["понедельник", "вторник", "среда", "четверг", "пятница", "текущая неделя",
                                    "следующая неделя", "/week", "/help", "/mtuci"]:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял.')


bot.infinity_polling()
