import telebot
from telebot import types
import hashlib
from hash import hash_alg
import time

hash_algorithms = sorted(hash_alg)

global algorihm_list
TOKEN = '729146636:AAGYpuJ45w0ZuetpCzBB5PDsOlNePDw7N7g'
bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True, row_width=3)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    mc = message.chat
    text = 'Hello '+f'{mc.first_name}'+'!'+' Choose any type of HASHING ALGORIHM and get your Genereted Hash Value!'
    for hash_a in hash_algorithms:
        markup.add(hash_a)
    bot.send_message(mc.id, text, reply_markup=markup)
#-----------------------------------------------------------------------
def hash_value_generate(algorihm_name, plain_text):
    hash_value = hashlib.new(f'{algorihm_name}') # setting algorithm
    byte_string = plain_text.encode('ASCII') # converting string into byte-string
    hash_value.update(byte_string) # getting hash object
    return hash_value.hexdigest() # getting hash hexdigest value
#-----------------------------------------------------------------------
@bot.message_handler(content_types=['text'])
def reply(message):
    cid = message.chat.id
    text = message.text
    if text in hash_algorithms:
        current_algorihm_name = text
        global algorihm_list
        algorihm_list = []
        algorihm_list.append(current_algorihm_name)
        bot.send_message(cid, f'Okay, you have chosen "{text}" ALGORIHM, then send me a TEXT that you want to be Hashed')
    else:
        plain_text = text
        bot.send_message(cid, "HERE YOU ARE:")
        bot.send_message(cid, hash_value_generate(algorihm_list[-1], plain_text))


def telegram_polling():
    try:
        bot.polling(none_stop=True, timeout=60) #constantly get messages from Telegram
    except:
        bot.stop_polling()
        time.sleep(10)
        telegram_polling()

if __name__ == '__main__':    
    telegram_polling()


