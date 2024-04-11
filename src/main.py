import pickle
from config import TOKEN
from info import price_text, info_text, greetings_text
import telebot

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_greetings(message):
    bot.send_message(message.chat.id, greetings_text)


@bot.message_handler(commands=['film'])
def send_film(message):
    messageEvenLoad = []
    messageOddLoad = []

    # Load the information from the file
    with open('saveEven.txt', 'rb') as file:
        messageEvenLoad = pickle.load(file)

    with open('saveOdd.txt', 'rb') as file:
        messageOddLoad = pickle.load(file)

    for elem in messageEvenLoad:
        bot.send_message(message.chat.id, elem)

    for elem in messageOddLoad:
        bot.send_message(message.chat.id, elem)


@bot.message_handler(commands=['prezzi'])
def send_price(message):
    bot.send_message(message.chat.id, price_text)


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, info_text)


bot.infinity_polling()
