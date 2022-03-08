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



if __name__ == "__main__":
    # Running server
    bot.send_message(chat_id=config['TELEGRAM']['ME'], text="睡觉吧，别像我一样入土了。") # need chat id
