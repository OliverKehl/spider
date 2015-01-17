# coding:utf-8
__author__='kehl'

import sys,os
sys.path.append(os.path.dirname(os.getcwd()))

import urllib2
from tables.models import CidianInfo
import time



host = 'http://hanyu.iciba.com'

def filter(str):
    str = str.replace('。','.')
    str = str.replace('～','~')
    str = str.replace('（','(')
    str = str.replace('）',')')
    str = str.replace('、',',')
    return str

#把gbk编码的字符串转换成utf8格式
#response = response.decode('gbk').encode('utf-8')

SIZE=1000

def crawlToFile(filename):
    f = open(filename,'r')
    reserved_words=[]
    not_exist_words = []
    cidianInfos = []
    count = 0
    lines = f.readlines()[1:]
    for i in range(len(lines)):
        line = lines[i]
        line = line.strip()
        if len(line.decode('utf8'))<2:
            continue
        try:
            url = 'http://hanyu.iciba.com/hy/'+line
            req = urllib2.urlopen(url)
            temp_str = req.url
            if temp_str.find('http://hanyu.iciba.com/hy/')<0:
                not_exist_words.append(line)
                continue
            response = req.read()
    
            start = response.find('url')+4
            end = response.rfind('shtml')+5
            target = host + response[start:end]
            req = urllib2.urlopen(target)
            s = req.read()
    
            shiyi = s.find('[释义]')
            if shiyi==-1:
                not_exist_words.append(line)
                continue
            f2 = open('output/'+str(i)+'.txt','w')
            f2.writelines(s)
            f2.close()
            time.sleep(3)
        except Exception , e:
            pass
    f.close()
if __name__=='__main__':
    import os,sys
    crawlToFile(os.path.dirname(os.getcwd())+'/data/vocab.txt')
    
        
        
