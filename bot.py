import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.token)

inline_keyboard = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton('Доход', callback_data='income')
btn2 = types.InlineKeyboardButton('Расход', callback_data='costs')
inline_keyboard.add(btn1, btn2)

info = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, f'Выберите категорию {message.chat.first_name}', reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda c: True)
def income(c):
    chat_id = c.message.chat.id
    if c.data == 'income':
        reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        repl1 = types.KeyboardButton('Работа')
        repl2 = types.KeyboardButton('Бизнес')
        repl3 = types.KeyboardButton('Другое')
        reply_keyboard.add(repl1, repl2, repl3)
        message = bot.send_message(chat_id, "Выберите способ заработка", reply_markup=reply_keyboard)
        bot.register_next_step_handler(message, get_category_income)

    elif c.data == 'costs':
        reply_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        repl1 = types.KeyboardButton('Продукты')
        repl2 = types.KeyboardButton('Дорога')
        repl3 = types.KeyboardButton('Другое')
        reply_keyboard.add(repl1, repl2, repl3)
        message = bot.send_message(chat_id, "Выберите ваши расходы", reply_markup=reply_keyboard)
        bot.register_next_step_handler(message, get_category_costs)


def get_category_costs(message):
    chat_id = message.chat.id
    info['category'] = message.text
    bot.send_message(chat_id, "Сумма ваших затрат")
    bot.register_next_step_handler(message,get_sum_costs)


def get_category_income(message):
    chat_id = message.chat.id
    info['category'] = message.text
    bot.send_message(chat_id, 'Сумма вашего заработка')
    bot.register_next_step_handler(message, get_sum_income)


def get_sum_costs(message):
    chat_id = message.chat.id
    info['sum'] = message.text
    bot.send_message(chat_id, 'Сумма расходов зафиксирована')
    print(info)


def get_sum_income(message):
    chat_id = message.chat.id
    info['sum'] = message.text
    bot.send_message(chat_id, 'Мы записали вашу сумму заработок')

    print(info)

# @bot.message_handler(content_types=['text'])
# def repeat_message(message):
#     if message.chat.type == 'private':
#         if message.text == 'Рандомное число':
#             bot.send_message(message.chat.id, str(random.randint(0, 100)))
#         elif message.text == 'Как дела?':
#
#             markup = types.InlineKeyboardMarkup(row_width=2)
#             item1 = types.InlineKeyboardButton('Хорошо', callback_data='good')
#             item2 = types.InlineKeyboardButton('Не очень', callback_data='bad')
#
#             markup.add(item1, item2)
#
#             bot.send_message(message.chat.id, 'Gooood', reply_markup=markup)
#         else:
#             bot.send_message(message.chat.id, 'Я не знаю эту команду')


    # print(message.chat.id)
    # print(message.text)
    # print(bot.get_me())
    # print(message.from_user)

# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     try:
#         if call.message:
#             # print(call.message)
#             if call.data == 'good':
#                 bot.send_message(call.message.chat.id, 'Вот и отличненько')
#                 print(call.data)
#             elif call.data == 'bad':
#                 bot.send_message(call.message.chat.id, 'Вот и отличненько')
#                 print()
#     except:
#         print("D")
# #
if __name__ == '__main__':
    bot.infinity_polling()
# bot.polling(none_stop=True)