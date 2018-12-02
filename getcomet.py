import os 
import re
import requests
import html2text
import numpy as np

h2t = html2text.HTML2Text()

def get_week():
    week_url = 'http://www.aerith.net/comet/weekly/current.html'
    week_r = requests.get(week_url).text
    # find all comet names
    all_name = re.findall('\<A HREF="\.\./catalog/[^\<\>]+"\>[^\<]+\</A\>',week_r)
    # find all comet infomation table
    all_info = re.findall('\<PRE\>[^\<\>]+\</PRE\>',week_r)
    text = ''
    for i in range(0,3):
        # the ith name
        name = re.findall('(?<=\>).*(?=\<)',all_name[i])
        # the ith info  table
        info = all_info[i]
        # remove useless strings
        info = info.replace('<PRE>\nDate(TT)  R.A. (2000) Decl.   Delta     r    Elong.  m1   Best Time(A, h)  \n','')
        info = info.replace('\n</PRE>','')
        # find all numbers in table
        info = re.findall(r'(?<= )[0-9\:\-\.]+(?= )',info)
        # select the newest mag and best time
        mag = info[-2]
        best_time = info[-1]
        # the text to be sent
        text += '*' + name[0] + '*' + ' ' + mag + ' mag  _best time: ' + best_time + '_' + '\n'
    
    return text


if __name__ == '__main__':
    print(get_week())