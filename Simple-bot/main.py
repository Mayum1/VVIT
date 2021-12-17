import telebot
import random
from telebot import types
from datetime import datetime

token = "telegram_bot_token"
bot = telebot.TeleBot(token)
day = datetime.now().strftime('%Y-%m-%d')
luckNum = random.randint(1, 100)
if luckNum == 1:
    luck = 'великая удача!'
elif luckNum == 2:
    luck = 'великая неудача!'
elif luckNum in range(3, 35):
    luck = 'удача!'
elif luckNum in range(35, 67):
    luck = 'неудача!'
elif luckNum in range(67, 101):
    luck = 'нейтральность!'


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу", "Проверка удачи", "/help", "/time")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'С помощью этого бота Вы можете узнать свою удачу на сегодняшний день, вывести '
                                      'рандомное число, а также узнать текущее время.\n\n'
                                      'Хочу - вывести ссылку на сайт MTUCI\n'
                                      'Проверка удачи - вывести удачу на сегодня\n'
                                      'Рандом n m - вывести рандомное число от n до m\n\n'
                                      '/time - вывести текущую дату и время\n'
                                      '/help - вывести это сообщение')


@bot.message_handler(commands=['time'])
def time_message(message):
    bot.send_message(message.chat.id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@bot.message_handler(content_types=['text'])
def answer(message):
    global day, luckNum, luck
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')

    elif message.text.capitalize() == "Проверка удачи":
        if datetime.now().strftime('%Y-%m-%d') != day:
            day = datetime.now().strftime('%Y-%m-%d')
            luckNum = random.randint(1, 100)
            if luckNum == 1:
                luck = 'великая удача!'
            elif luckNum == 2:
                luck = 'великая неудача!'
            elif luckNum in range(3, 35):
                luck = 'удача!'
            elif luckNum in range(35, 67):
                luck = 'неудача!'
            elif luckNum in range(67, 101):
                luck = 'нейтральность!'
            bot.send_message(message.chat.id, 'Сегодня Вам сопутствует ' + str(luck))
        else:
            bot.send_message(message.chat.id, 'Сегодня Вам сопутствует ' + str(luck))
    elif 'рандом' in message.text.lower():
        if message.text.lower() == 'рандом':
            bot.send_message(message.chat.id, 'Введите от какого до какого числа. Пример: 1 20')
        else:
            n = message.text.find(' ')
            numbs = message.text[n:].split()
            numb1 = int(numbs[0])
            numb2 = int(numbs[1])
            bot.send_message(message.chat.id, str(random.randint(numb1, numb2)))


bot.infinity_polling()
