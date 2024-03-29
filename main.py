import configparser
import logging

import numpy as np
import telegram
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler

import getapod
import getcomet
import getmoon
import getmercury
import meteoblue
import ephemeris

# Load data from config.ini file
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


# def reply_handler(bot, update):
#     """Reply message."""
#     text = update.message.text
#     update.message.reply_text(text)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="周末晴天无月夜？不存在的。——郭守敬")


def obs(bot, update, args):
    obj_name = args[0]
    try:
        day_offset = args[1]
    except:
        day_offset = None
    bot.send_message(chat_id=update.message.chat_id, text=ephemeris.ephemeris(
        obj_name, day_offset), parse_mode='Markdown')


def meteo(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=meteoblue.get_meteo())


def startapod(bot, update):
    id = np.loadtxt('id.txt', dtype=int)
    if np.sum(id == update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id, text="订阅成功")
    else:
        np.savetxt('id.txt', np.append(id, update.message.chat_id), fmt='%.0f')
        bot.send_message(chat_id=update.message.chat_id, text="订阅成功")


def apod(bot, update, args):
    date = ''.join(args)
    if date == '':
        url = 'https://apod.nasa.gov/apod/astropix.html'
        url_zh = 'http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/apod.html'
    else:
        url = 'https://apod.nasa.gov/apod/ap' + date + '.html'
        url_zh = 'http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/ap' + date + '.html'

    bot.send_message(chat_id=update.message.chat_id,
                     text=getapod.get_pic(url_zh))
    bot.send_message(chat_id=update.message.chat_id,
                     text=getapod.get_exp(url_zh, 'zh'), parse_mode='Markdown')


def stopapod(bot, update):
    id = np.loadtxt('id.txt', dtype=int)
    id = np.delete(id, np.argwhere(id == update.message.chat_id))
    np.savetxt('id.txt', id, fmt='%.0f')

    bot.send_message(chat_id=update.message.chat_id, text="已取消")


def cometweekly(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=getcomet.get_week(), parse_mode='Markdown')


def moonphase(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=getmoon.get_moonphase())


def mercury(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=getmercury.get_mercury())


# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
# dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

# start command reply
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# get object altitude at night and the moon's altitude
obs_handler = CommandHandler('obs', obs, pass_args=True)
dispatcher.add_handler(obs_handler)

# get the meteoblue 5-days diagram of our remote observatory
meteo_handler = CommandHandler('meteo', meteo)
dispatcher.add_handler(meteo_handler)

# apod command
apod_handler = CommandHandler('apod', apod, pass_args=True)
dispatcher.add_handler(apod_handler)

# startapod command
startapod_handler = CommandHandler('startapod', startapod)
dispatcher.add_handler(startapod_handler)

# stopapod command
stopapod_handler = CommandHandler('stopapod', stopapod)
dispatcher.add_handler(stopapod_handler)

# cometweekly command
cometweekly_handler = CommandHandler('cometweekly', cometweekly)
dispatcher.add_handler(cometweekly_handler)

# moonphase command
moonphase_handler = CommandHandler('moonphase', moonphase)
dispatcher.add_handler(moonphase_handler)

# mercury command
mercury_handler = CommandHandler('mercury', mercury)
dispatcher.add_handler(mercury_handler)


if __name__ == "__main__":
    # Running server
    app.run()
