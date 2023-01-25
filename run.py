import threading
import time
import telebot
import logging


def remove_new_line(s):
    return s.replace("\n", "")


def time_pooling_thread():
    while True:
        time.sleep(2)
        print("Current time: %s" % (time.ctime(time.time())))


def init_log():
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('Telegram Bot V0.1 was started')


settings = open('../token.txt', 'r')

token = remove_new_line(settings.readline())
password = remove_new_line(settings.readline())
logfile = remove_new_line(settings.readline())

init_log()

bot = telebot.TeleBot(token)

try:
    threading.Thread(target=time_pooling_thread).start()
except Exception as e:
    logging.error("Error: unable to start thread" + e)

while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        logging.error("Error: " + e)
        time.sleep(15)
