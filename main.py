import configparser
import logging

import telegram
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler

import getapod
import getcomet
import getmoon
import getmercury

# Load data from config.ini file
config = configparser.ConfigParser()
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


def reply_handler(bot, update):
    """Reply message."""
    text = update.message.text
    update.message.reply_text(text)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="周末晴天无月夜？不存在的。——郭守敬")
    
def startapod(bot,update):
    with open('id.txt','a+') as id:
        id.write(str(update.message.chat_id)+'\n')
    
    bot.send_message(chat_id=update.message.chat_id, text="订阅成功")
    

def apod(bot, update, args):
    date = ''.join(args)
    if date =='':
        url = 'https://apod.nasa.gov/apod/astropix.html'
        url_zh = 'http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/apod.html'
    else:
        url = 'https://apod.nasa.gov/apod/ap'+ date + '.html'
        url_zh = 'http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/ap' + date + '.html'
        
    bot.send_message(chat_id=update.message.chat_id, text= getapod.get_pic(url))
    bot.send_message(chat_id=update.message.chat_id, text= getapod.get_exp(url_zh,'zh'), parse_mode='Markdown')
    
def stopapod(bot,update):
    with open('id.txt','r') as id:
        idstr = id.read()
        idstr = idstr.replace(str(update.message.chat_id)+'\n','')
    
    with open('id.txt','w') as id:
        id.write(idstr)
        
    bot.send_message(chat_id=update.message.chat_id, text="已取消")

def cometweekly(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text= getcomet.get_week(), parse_mode='Markdown')
    
def moonphase(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text= getmoon.get_moonphase())
    
def mercury(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text= getmercury.get_mercury())
    
# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

# start command reply
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

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
