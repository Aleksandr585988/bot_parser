# import queue
# import time
# import threading
# from aiogram import types
# from aiogram.enums import ParseMode
# from aiogram.utils.markdown import hlink
# from config import token
# from telebot import types
# import telebot
# import json
# from parser_it import check_news_update_it
# from parser_space import check_news_update_space
# bot = telebot.TeleBot(token, parse_mode=ParseMode.HTML, threaded=True)
#
#
# chat_ids = []
#
#
# @bot.message_handler(commands=['start'])  # t2
# def start(message):
#     if message.chat.id not in chat_ids:
#         chat_ids.append(message.chat.id)
#         print("START!!!!")
#         print(chat_ids)
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#         start_button1 = types.KeyboardButton('/fresh_it')
#         start_button2 = types.KeyboardButton('/fresh_space')
#         start_button3 = types.KeyboardButton('/all_it')
#         start_button4 = types.KeyboardButton('/all_space')
#         keyboard.add(start_button1, start_button2, start_button3, start_button4)
#         bot.send_message(message.chat.id, 'Виберите новости', reply_markup=keyboard)
#
#
# @bot.message_handler(commands=['all_it'])
# def get_all_news_it(message: types.Message):
#     print('all_it')
#     with open("news_dict_it.json") as f:
#         news_dict = json.load(f)
#
#     for k, v in reversed(news_dict.items()):
#         news = (f"<u>{v['published']}</u>\n"
#                 f"{hlink(v['article_title'],v['article_url'])}\n")
#
#         bot.send_message(message.chat.id, news)
#
#
# @bot.message_handler(commands=['fresh_it'])
# def get_last_news_it(message: types.Message):
#     while True:
#         fresh_news = check_news_update_it()
#         if len(fresh_news) >= 1:
#             for k, v in reversed(fresh_news.items()):
#                 news = (f"{v['published']}\n"
#                         f"{hlink(v['article_title'], v['article_url'])}\n")
#                 msg_queue.put(news)
#
# #                bot.send_message(message.chat.id, news)
#         print('fresh it')
#         time.sleep(55)
#
#
# @bot.message_handler(commands=['all_space'])
# def get_all_news_space(message: types.Message):
#     with open("news_dict_space.json") as f:
#         news_dict_space = json.load(f)
#
#     for k, v in reversed(news_dict_space.items()):
#         news_space = (f"<u>{v['time']}</u>\n"
#                       f"{hlink(v['title'],v['link'])}\n")
#
#         bot.send_message(message.chat.id, news_space)
#
#
# @bot.message_handler(commands=['fresh_space'])
# def get_last_news_space(message: types.Message):
#     while True:
#         fresh_news_space = check_news_update_space()
#         if len(fresh_news_space) >= 1:
#             for k, v in reversed(fresh_news_space.items()):
#                 news_space = (f"{v['time']}\n"
#                               f"{hlink(v['title'], v['link'])}\n")
#                 msg_queue.put(news_space)
#
# #                bot.send_message(message.chat.id, 'www', news_space)
#         print('fresh space')
#         time.sleep(50)
#
#
# def msg_sender(q):
#     while True:
#         message = q.get()
#         for chat_id in chat_ids:
#             bot.send_message(chat_id, message)
# #        print("send message ", message)
#
#
# t = threading.Thread(target=bot.polling).start()
# msg_queue = queue.Queue()
#
# t1 = threading.Thread(target=msg_sender, args=(msg_queue,))
# t1.start()
#
# t2 = threading.Thread(target=get_last_news_it, args=(msg_queue,))
# t2.start()
#
# t3 = threading.Thread(target=get_last_news_space, args=(msg_queue,))
# t3.start()
#
# t = time.time()
#
# while True:
#     if time.time() - t > 10:
#         print("1234")
#         t = time.time()
# #        msg_queue.put(f"test message {time.time()}")
