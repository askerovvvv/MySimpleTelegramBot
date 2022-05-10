import telebot
import config
import random
import csv
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
    list_of_stickers = ['CAACAgIAAxkBAAEEsdlieoFe62ogzoI028UQI2UIIDVTlgACRwADWbv8JVyd1qxN32EsJAQ', 'CAACAgIAAxkBAAEEsd9ieoF3lP5aM5006B5eQEOG_MEQ1wACBQADwDZPE_lqX5qCa011JAQ']
    bot.send_sticker(chat_id, random.choice(list_of_stickers))


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
    stickers = [
        'CAACAgIAAxkBAAEEseFieoF9vZGwljRu_qcRb-IpMVx3MwACIAADwDZPE_QPK7o-X_TPJAQ',
        'CAACAgIAAxkBAAEEseVieoLMhw5MOcvV6su3g1VcME3GHAACTAADWbv8JfRkx3MXxG1fJAQ',
        'CAACAgIAAxkBAAEEsedieoLQ3-szQ9OszjQJwrnW8XNizgACEQADwDZPEw2qsw_cHj7lJAQ',
    ]

    chat_id = message.chat.id
    info['sum'] = message.text

    csv_file = 'costs.csv'
    with open(csv_file, 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((info['category'], info['sum']))

    bot.send_message(chat_id, 'Сумма расходов зафиксирована')
    bot.send_sticker(chat_id, random.choice(stickers))


def get_sum_income(message):
    stickers = [
        'CAACAgIAAxkBAAEEsd1ieoF1VMGEi5vGhDQRhNLRrcyGFQACFQADwDZPE81WpjthnmTnJAQ',
        'CAACAgIAAxkBAAEEsdtieoFkaOuQBw0znuS_GnSdJtAENQACRQADWbv8JfvUpDThE_jrJAQ',
    ]

    chat_id = message.chat.id
    info['sum'] = message.text

    csv_file = 'income.csv'
    with open(csv_file, 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((info['category'], info['sum']))

    bot.send_message(chat_id, 'Мы записали вашу сумму заработок')
    bot.send_sticker(chat_id, random.choice(stickers))



if __name__ == '__main__':
    bot.infinity_polling()
# bot.polling(none_stop=True)