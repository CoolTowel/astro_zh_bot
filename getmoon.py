import time
import requests

user_timezone = -8
#设定用户时区, 默认为东八区
user_timestamp = time.time() + 3600 * user_timezone
#获取时间戳, 并按照用户时区进行偏移
user_time = time.localtime(user_timestamp)
#格式化用户时间
user_year = time.strftime('%Y', user_time)
#获取用户年份
user_month = time.strftime('%m', user_time)
#获取用户月份
user_date = time.strftime('%d', user_time)
#获取用户日期
user_time_1st = time.strptime(str(user_year) + '-' + str(user_month) + '-' + '1', '%Y-%m-%d')
#用户时区当月1日的格式化时间
LDZ = int(time.mktime(user_time_1st))
#获取LDZ, 即按时区偏移后的当月1日零时时间戳取整

url = 'http://www.icalendar37.net/lunar/api/?lang=en&month=' + str(user_month) + '&year=' + str(user_year) + '&size=100&lightColor=rgb(255,255,255)&shadeColor=rgb(17,17,17)&LDZ=' + str(LDZ)
#生成url

dict = {'New Moon':'新月', 'First quarter':'上弦月', 'Last quarter':'下弦月', 'Full moon':'满月'}
#部分月相名称字典


def round_new(value):
    #替换内置round函数, 实现保留2位小数的精确四舍五入
    return round(value * 100) / 100.0


def get_moonphase():
    try:
        data = requests.get(url).json()
        #读取网页json数据
        
    except BaseException:
        output = '月相获取失败，请稍后重试。'
        return output
        #异常处理
        
    else:
        phasename = data['phase'][str(user_date)]['phaseName']
        #获取当日月相名称
        pctillum = round_new(data['phase'][str(user_date)]['lighting'])
        #获取月相百分比并保留两位小数
        if phasename in dict.keys():
            phasename = dict[phasename]
        #新月, 上弦月, 下弦月与满月
        elif phasename == 'Waxing':
            if pctillum < 50:
                phasename = '蛾眉月'
            elif pctillum > 50:
                phasename = '盈凸月'
        elif phasename == 'Waning':
            if pctillum > 50:
                phasename = '亏凸月'
            elif pctillum < 50:
                phasename = '残月'
        #蛾眉月, 盈凸月, 亏凸月与残月
        output = phasename + ' ' + str(pctillum) + '%'
        #输出月相名称及百分比
        return output
        #返回结果


if __name__ == '__main__':
    print(get_moonphase())
    #本地调试输出