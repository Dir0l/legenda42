import telebot
import random
from config import TOKEN
import time
import threading,schedule

from telebot import TeleBot

API_TOKEN = '<api_token>'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'hi'])
def start_message(message):
    bot.reply_to(message, 'Привет, я тестовый бот!')

@bot.message_handler(commands=['password'])
def gen_pass(message):
    elements = '+-/*!&$#?=@<>123456789'
    password = ''
    for i in range(10):
        password += random.choice(elements)
    bot.send_message(message.chat.id, password)

@bot.message_handler(commands=['coin'])
def coin(message):
    a = random.randint(1,3)
    if a == 1:
        bot.reply_to(message, 'Орёл')
    else:
        bot.send_message(message.chat.id, 'Решка')



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hi! Use /set <seconds> to set a timer")


def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Beep!')


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)




@bot.message_handler(func=lambda message: True)
def any_message(message):
    bot.send_message(message.chat.id, message.text)


bot.infinity_polling()
