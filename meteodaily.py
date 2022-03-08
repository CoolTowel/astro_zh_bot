import time
import configparser
import telegram
import meteoblue
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))


def job():
    bot.send_message(chat_id=config['TELEGRAM']
                     ['KART'], text=meteoblue.get_meteo())


scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='0-6', hour=19, minute=00)
scheduler.start()
