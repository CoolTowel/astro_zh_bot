import time
import configparser
import telegram
import getapod
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

bot = telegram.Bot(token = (config['TELEGRAM']['ACCESS_TOKEN']))

url = config['WEBSITE']['METEO_GAOYAZI']

def job():
    bot.send_message(chat_id = config['WEBSITE']['ME'], text = url)
    

scheduler = BlockingScheduler()
scheduler.add_job(job,'cron', day_of_week='0-6', hour=19, minute=00)
scheduler.start()
