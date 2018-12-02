import os 
import re
import requests
import html2text
from hanziconv import HanziConv


def get_pic(url):
    r = requests.get(url).text
    found = re.findall('image/.*.jpg',r)
    pic_url = 'https://apod.nasa.gov/apod/' + found[-1]
    return pic_url
	
def get_exp(url,lan):
    if lan == 'zh': 
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        r = r.text
        r = r.replace('\n','')
        exp = re.findall('\d\d\d\d 年.*<p> <center>',r)[0]
        h2t = html2text.HTML2Text()
        h2t.ignore_links = True
        exp = HanziConv.toSimplified(h2t.handle(exp))
        mv = re.findall('![^我可去你妈的正则表达式]*\)',exp)[0]
        exp = exp.replace(mv,'\n')
        exp = exp.replace('**','*')
        return exp
    else:
        url = 'https://apod.nasa.gov/apod/astropix.html'
        r = requests.get(url)
        r = r.text
        r = r.replace('\n','')
        exp = re.findall('</center> <p>.*<b> Explanation: </b>.*<p> <center>',r)[0]
        h2t = html2text.HTML2Text()
        h2t.ignore_links = True
        exp = h2t.handle(exp)
        return exp

if __name__ == '__name__':
    print(get_pic()+'\n'+get_exp('http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/apod.html',zh))