# coding:utf-8
__author__='kehl'

import urllib2
import config
from tables.models import CidianInfo
from tables import DBSession



host = 'http://hanyu.iciba.com'
def crawl(file):
    f = open(file,'r')
    session = DBSession()
    for line in f.readlines():
        line = line.strip()
        url = 'http://hanyu.iciba.com/hy/'+line
        req = urllib2.urlopen(url)
        response = req.read()
        
        
        #把gbk编码的字符串转换成utf8格式
        #response = response.decode('gbk').encode('utf-8')

        #page jump
        start = response.find('url')+4
        end = response.rfind('shtml')+5
        target = host + response[start:end]
        req = urllib2.urlopen(target)
        s = req.read()
        start = s.find('[释义]')
        end = s.find('div',start)
        print s[start:end-1].strip()
        

if __name__=='__main__':
    crawl('/home/kehl/vocabs.txt')
        
        