import os 
import re
import requests
import html2text
import opencc


def get_pic(url):
    r = requests.get(url).text
    p = re.compile('SRC=\"image(.*?\.jpg)\"')
    pic = p.findall(r)
    if pic:
        pic_url = 'http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/image' + pic[-1]
        return pic_url
    else:
        v = re.compile('src=\"(.*?rel\=0)\"')
        video = v.findall(r)
        return video[0]

def get_exp(url,lan):
    if lan == 'zh': 
        converter = opencc.OpenCC('t2s.json')
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        r = r.text
        r = r.replace('\n','')
        date = re.findall('\d\d\d\d ?年 ?\d+ ?月 ?\d+ ?日',r)[0] #find the date of APOD
        h2t = html2text.HTML2Text()
        h2t.ignore_links = True
        exp = re.findall('</center>[\s]{0,}<center>[\s\S]+<p> ?<center>',r)[0] #find the explanation of APOD 
        exp = converter.convert(h2t.handle(exp))
        explist = exp.split('**说明:**')
        exp1 = explist[0]
        exp2 = explist[1].replace('\n','')
        exp = exp1 + '*说明：*' +exp2
        exp = exp.replace('**','*')
        return date + '\n\n' + exp
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

if __name__ == '__main__':
    pic = get_pic('https://apod.nasa.gov/apod/astropix.html')
    print(pic)
    exp = get_exp('http://sprite.phys.ncku.edu.tw/astrolab/mirrors/apod/apod.html','zh')
    print(r''+exp)

