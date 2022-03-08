import requests as req
from PIL import Image
from io import BytesIO
import time
import configparser

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

website = config['WEBSITE']['WEBSITE_URL']
yunling_src = config['WEBSITE']['METEO_YUNLING']


def get_meteo():
    # 云岭台
    img_src = yunling_src
    response = req.get(img_src)
    image = Image.open(BytesIO(response.content))
    ticks = time.strftime('%Y_%m_%d_%H', time.localtime(time.time()))
    web_path = '/var/www'
    path = '/meteoblue/yunling/'+str(ticks)+'.png'  # 云岭台
    url = website+path
    image.save(web_path+path)
    return url


if __name__ == '__main__':
    print(get_meteo())
