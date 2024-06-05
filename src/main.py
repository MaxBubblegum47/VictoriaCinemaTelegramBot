'''
This is code that handles the telegram bot. As you can see there are several functions.
Each of them control one function of the bot. At the beggining the bot load the API Key.
The Key is inside the config.py file. 
'''

import pickle
from config import TOKEN
from info import price_text, info_text, greetings_text
import telebot

bot = telebot.TeleBot(TOKEN)

# Greetgins message for the user
@bot.message_handler(commands=['start'])
def send_greetings(message):
    bot.send_message(message.chat.id, greetings_text)

# List of all the available movies in the teather
@bot.message_handler(commands=['film'])
def send_film(message):
    messageEvenLoad = []
    messageOddLoad = []

    # Load the available messages. It cannot happen that there are no .txt files
    # because the bash orchestrator check for it in advance
    with open('saveEven.txt', 'rb') as file:
        messageEvenLoad = pickle.load(file)

    with open('saveOdd.txt', 'rb') as file:
        messageOddLoad = pickle.load(file)

    for elem in messageEvenLoad:
        bot.send_message(message.chat.id, elem)

    for elem in messageOddLoad:
        bot.send_message(message.chat.id, elem)

# Gives the user all the info related with prices. Those informations
# are directly taken from the info.py file.
@bot.message_handler(commands=['prezzi'])
def send_price(message):
    bot.send_message(message.chat.id, price_text)

# Gives the user all the info that are no related with prices, like discounts and other stuff. 
# Those informations are directly taken from the info.py file.
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, info_text)


bot.infinity_polling()
