import threading
import time
import telebot


def remove_new_line(s):
    return s.replace("\n", "")


def time_pooling_thread():
    print('Time pooling thread was started')
    while True:
        time.sleep(2)
        print("Current time: %s" % (time.ctime(time.time())))


print("Telegram Bot V0.1")

settings = open('../token.txt', 'r')

token = remove_new_line(settings.readline())
password = remove_new_line(settings.readline())
logfile = remove_new_line(settings.readline())

bot = telebot.TeleBot(token)

try:
    threading.Thread(target=time_pooling_thread).start()
except Exception as e:
    print("Error: unable to start thread" + e)

while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        time.sleep(15)
