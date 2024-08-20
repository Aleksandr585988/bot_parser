import queue
import time
import threading
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hlink
from config import token
from telebot import types
import telebot
import json
import webbrowser
from parser_it import check_news_update_it
from parser_space import check_news_update_space

bot = telebot.TeleBot(token, parse_mode=ParseMode.HTML, threaded=True)


@bot.message_handler(commands=['start'])
def start(message):
    a = open('id_file.txt')
    a1 = a.read().split()
    b = str(message.chat.id)
    if b in a1:
        print('es')
        print('START!!!!')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_button1 = types.KeyboardButton("/news_it")
        start_button2 = types.KeyboardButton("/news_space")
        start_button3 = types.KeyboardButton("Ваши данные")
        start_button4 = types.KeyboardButton("Ваш id")
        start_button5 = types.KeyboardButton("/site_it_news")
        start_button6 = types.KeyboardButton("/site_space_news")
        keyboard.add(start_button1, start_button2, start_button3, start_button4, start_button5,
                     start_button6)
        bot.send_message(message.chat.id, f'Привет: {message.from_user.first_name} {message.from_user.last_name}! 👋🏼')
        bot.send_message(message.chat.id, '<b><u>Виберите новости</u></b>', reply_markup=keyboard, parse_mode='html')

    else:
        print('no')
        a = open('id_file.txt', 'a')
        b = int(message.chat.id)
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        a.write(f'{last_name} {first_name}, {b}\n')
        a.close()
        print("START!!!!")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_button1 = types.KeyboardButton('/news_it')
        start_button2 = types.KeyboardButton('/news_space')
        start_button3 = types.KeyboardButton('Ваши данные')
        start_button4 = types.KeyboardButton('Ваш id')
        start_button5 = types.KeyboardButton('/site_it_news')
        start_button6 = types.KeyboardButton('/site_space_news')
        keyboard.add(start_button1, start_button2, start_button3, start_button4, start_button5,
                     start_button6)
        bot.send_message(message.chat.id, f'Привет: {message.from_user.first_name} {message.from_user.last_name}!')
        bot.send_message(message.chat.id, 'Виберите новости', reply_markup=keyboard)


@bot.message_handler(commands=['site_it_news'])
def site_it_news(message):
    webbrowser.open_new('https://speka.media/news-'
                        'it?utm_source=google&utm_medium=cpc&utm_campaign=21107681931&gad_source=1')


@bot.message_handler(commands=['site_space_news'])
def site_space_news(message):
    webbrowser.open_new('https://www.unian.ua/tag/kosmos')


@bot.message_handler(commands=['news_it'])
def get_all_news_it(message: types.Message):
    t2 = threading.Thread(target=get_last_news_it, args=(msg_queue,))
    t2.start()
    print('all_it')
    with open("news_dict_it.json") as f:
        news_dict = json.load(f)

    for k, v in reversed(news_dict.items()):
        news = (f"<u>{v['published']}</u>\n"
                f"{hlink(v['article_title'],v['article_url'])}\n")

        bot.send_message(message.chat.id, news)


def get_last_news_it(message):
    while True:
        fresh_news = check_news_update_it()
        if len(fresh_news) >= 1:
            for k, v in reversed(fresh_news.items()):
                news = (f"{v['published']}\n"
                        f"{hlink(v['article_title'], v['article_url'])}\n")

                bot.send_message(message.chat.id, news)
        print('fresh it')
        time.sleep(30)


@bot.message_handler(commands=['news_space'])
def get_all_news_space(message):
    t2 = threading.Thread(target=get_last_news_space, args=(msg_queue,))
    t2.start()
    with open("news_dict_space.json") as f:
        news_dict_space = json.load(f)

    for k, v in reversed(news_dict_space.items()):
        news_space = (f"<u>{v['time']}</u>\n"
                      f"{hlink(v['title'],v['link'])}\n")

        bot.send_message(message.chat.id, news_space)


def get_last_news_space(message):
    while True:
        fresh_news_space = check_news_update_space()
        if len(fresh_news_space) >= 1:
            for k, v in reversed(fresh_news_space.items()):
                news_space = (f"{v['time']}\n"
                              f"{hlink(v['title'], v['link'])}\n")

                bot.send_message(message.chat.id, news_space)
        print('fresh space')
        time.sleep(30)


@bot.message_handler()
def text_processor(message):
    if message.text == 'Ваши данные':
        bot.send_message(message.chat.id, f'Ваши данные: {message.from_user.first_name} {message.from_user.last_name}!')
    elif message.text == 'Ваш id':
        bot.send_message(message.chat.id, f'Ваш id: {message.from_user.id}!')


t = threading.Thread(target=bot.polling).start()
msg_queue = queue.Queue()

t = time.time()

while True:
    if time.time() - t > 10:
        print("1234")
        t = time.time()
