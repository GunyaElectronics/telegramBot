import threading
import time
import telebot
import logging
from my_localisation import MyLocalisation
from activity import Activity

bot_is_running = False
content_type_text_handler = None


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


loc = MyLocalisation('../localisation.txt', encoding="utf8")
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
        bot.send_message(message.chat.id, loc.get_text('Incorrect format'))
    elif s[1] != password:
        bot.send_message(message.chat.id, loc.get_text('Incorrect passwd'))
    else:
        bot.send_message(message.chat.id, loc.get_text('Bot will be stopped'))
        bot_is_running = False
        bot.stop_polling()


def units_for_new_activity(message):
    bot.send_message(message.chat.id,
                     f'{message.text} {loc.get_text("units will be used for logging your new activity")}')
    global content_type_text_handler
    content_type_text_handler = None


def new_activity_message(message):
    bot.send_message(message.chat.id, f'{message.text} {loc.get_text("activity added successfully")}')
    bot.send_message(message.chat.id, f'{loc.get_text("What are the units of measurement for")} {message.text}?')
    global content_type_text_handler
    content_type_text_handler = units_for_new_activity


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     f'{loc.get_text("Hello")} {message.chat.first_name} {message.chat.last_name}')


@bot.message_handler(commands=['new'])
def new_activity(message):
    global content_type_text_handler
    content_type_text_handler = new_activity_message
    bot.send_message(message.chat.id, loc.get_text('Please, enter your new activity name'))


@bot.message_handler(content_types='text')
def message_text(message):
    global content_type_text_handler
    if content_type_text_handler:
        content_type_text_handler(message)
    else:
        print('this text not handled')


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
