import re
import requests

url = 'https://mercuryretrogradeapi.com/'

def get_mercury():
    r = requests.get(url).json()
    text =''
    if r['is_retrograde']:
        text += "老夫掐指一算，今日水逆。"
    else:
        text += "老夫掐指一算，今日没有水逆。"
    
    return text

if __name__ == '__main__':
    print(get_mercury())

