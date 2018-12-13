import telebot
from telebot import apihelper



access_token = '684350661:AAGGrzFvaAdiKpEQcd6OVdr6Bu8JKVISTyQ'
bot = telebot.TeleBot(access_token)

apihelper.proxy = {'https':'socks5://82.146.236.38:9999'}

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
