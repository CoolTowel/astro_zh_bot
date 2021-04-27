import time
import configparser
import telegram
import getapod
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler

config = configparser.ConfigParser()
config.read('config.ini')

bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))

url = "https://my.meteoblue.com/visimage/meteogram_web_hd?look=KILOMETER_PER_HOUR%2CCELSIUS%2CMILLIMETER&apikey="


def job():
    bot.send_message(chat_id=ID, text=url)


scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='0-6', hour=19, minute=00)
scheduler.start()
