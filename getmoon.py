#Moon Phase Module for astro_zh_bot(郭守敬) in Telegram

import time
from datetime import datetime
import requests

dict = {'New Moon':'🌑  新月', 'First quarter':'🌓  上弦月', 'Last quarter':'🌗  下弦月', 'Full moon':'🌕  满月'}
#部分月相名称字典

def round_new(value):
    #替换内置round函数, 实现保留2位小数的精确四舍五入
    return round(value * 100) / 100.0

def get_time(timezone):
    #根据用户时区, 返回用户时间的年月日及LDZ; ⚠️服务器时间默认为UTC时间
    timestamp = time.time()
    #获取时间戳
    user_time = timestamp + 3600 * timezone
    #根据用户时区对时间戳进行偏移
    date = datetime.fromtimestamp(user_time).day
    #获取用户日期
    month = datetime.fromtimestamp(user_time).month
    #获取用户月份
    year = datetime.fromtimestamp(user_time).year
    #获取用户年份
    LDZ = int(datetime(year, month, 1).timestamp() - 3600 * timezone)
    #获取LDZ, 即用户时区当月1日0时时间戳取整
    return date, month, year, LDZ

def get_moonphase():
    user_timezone = 8
    #用户时区, 默认为东八区
    (date, month, year, LDZ) = get_time(user_timezone)
    #获取用户年月日及LDZ
    url = 'http://www.icalendar37.net/lunar/api/?lang=en&month=' + str(month) + '&year=' + str(year) + '&size=100&lightColor=rgb(255,255,255)&shadeColor=rgb(17,17,17)&LDZ=' + str(LDZ)
    #生成url
    try:
        data = requests.get(url).json()
        #读取网页json数据 
    except BaseException:
        output = '月相获取失败，请稍后重试。'
        return output
        #异常处理 
    else:
        phasename = data['phase'][str(date)]['phaseName']
        #获取当日月相名称
        pctillum = round_new(data['phase'][str(date)]['lighting'])
        #获取月相百分比并保留两位小数
        if phasename in dict.keys():
            phasename = dict[phasename]
        #新月, 上弦月, 下弦月与满月
        elif phasename == 'Waxing':
            if pctillum < 50:
                phasename = '🌒  蛾眉月'
            elif pctillum > 50:
                phasename = '🌔  盈凸月'
        elif phasename == 'Waning':
            if pctillum > 50:
                phasename = '🌖  亏凸月'
            elif pctillum < 50:
                phasename = '🌘  残月'
        #蛾眉月, 盈凸月, 亏凸月与残月
        output = phasename + '  ' + str(pctillum) + "%"
        #输出月相名称及百分比
        return output
        #返回结果

if __name__ == '__main__':
    print(get_moonphase())
    #本地调试输出