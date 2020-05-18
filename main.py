import requests
import json

responseUrl = "https://cid.yandex.net/v7/info?phonenums={}&verticals=geo%2Cugc&lang=ru&lr=139913"

#подключение токена из файла .env
import os
from dotenv import load_dotenv
load_dotenv()
telegram_bot_token = os.getenv("telegram_bot_token")


import telebot
bot = telebot.TeleBot(telegram_bot_token)


def getCallerInfo(message, phone_number):
    response = requests.get(responseUrl.format(phone_number))
    response = response.text
    response = json.loads(response)
    send_text = "Информация о номере:\n"
    
    try:
        phonenum = response[0]["phonenum"]
        send_text = send_text + "Номер : " + phonenum + "\n"
    except:
        pass
    
    try:
        status = response[0]["result"]["ugc"]["status"]
        send_text = send_text + "Статус : " + status + "\n"
    except:
        pass
    
    try:
        polarity = response[0]["result"]["ugc"]["polarity"]
        send_text = send_text + "Полярность : " + polarity + "\n"
    except:
        send_text = send_text + "Доверие : " + "неизвестно" + "\n"

    try:
        verdict = response[0]["result"]["ugc"]["verdict"]
        send_text = send_text + "Решение : " + verdict + "\n"
    except:
        send_text = send_text + "Решение : " + "неизвестно" + "\n"

    try:
        description = response[0]["result"]["ugc"]["description"]
        send_text = send_text + "Описание : " + description + "\n"
    except:
        send_text = send_text + "Описание : " + "неизвестно" + "\n"
    

    bot.send_message(message.chat.id, send_text)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    getCallerInfo(message, message.text)


bot.polling(none_stop=True, interval=0)