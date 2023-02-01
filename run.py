import threading
import time
import telebot
import logging

bot_is_running = False


def remove_new_line(s):
    return s.replace("\n", "")


def time_pooling_thread():
    while bot_is_running:
        time.sleep(60)
        print("Current time: %s" % (time.ctime(time.time())))
    print('Destroy time pooling thread')


def init_log():
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('Telegram Bot V0.1 was started')


settings = open('../token.txt', 'r')

token = remove_new_line(settings.readline())
password = remove_new_line(settings.readline())
logfile = remove_new_line(settings.readline())

settings.close()

init_log()

bot_is_running = True

bot = telebot.TeleBot(token)


# Command format "/stop password"
@bot.message_handler(commands=['stop'])
def stop_message(message):
    global bot_is_running
    s = message.text.split()
    if s.__len__() != 2:
        bot.send_message(message.chat.id, 'Incorrect format')
    elif s[1] != password:
        bot.send_message(message.chat.id, 'Incorrect passwd')
    else:
        bot.send_message(message.chat.id, 'Bot will be stopped')
        bot_is_running = False
        bot.stop_polling()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     f'Hello {message.chat.first_name} {message.chat.last_name}')


try:
    threading.Thread(target=time_pooling_thread).start()
except Exception as e:
    logging.error("Error: unable to start thread" + e.__str__())

while True:
    try:
        bot.polling(none_stop=True)
        if not bot_is_running:
            print('exit 0')
            exit(0)
    except Exception as e:
        logging.error("Error: " + e.__str__())
        time.sleep(1)
