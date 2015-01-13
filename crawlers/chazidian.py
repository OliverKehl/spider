# coding:utf-8
import urllib2
import urllib

import config
def crawl(file):
    f = open(file,'r')
    for line in f.readlines():
        line = line.strip()
        url = 'http://www.chazidian.com/ci/?q='+line
        req = urllib2.urlopen(url)
        response = req.read()

        #把gbk编码的字符串转换成utf8格式
        #response = response.decode('gbk').encode('utf-8')

        #page jump
        offset =  response.find('title=\"'+ line +'\">')
        target_url = response[(offset-65):(offset-2)]
        req = urllib2.urlopen(target_url)
        response = req.read()
        temp = '<div class=\"text\"><h2 id=\"1\">基本解释'
        start = response.find(temp)+len(temp)
        end = response.find('</div></div>',start)
        res = response[start:end]
        print res

def post():
    url='http://www.chazidian.com/ci/?q=%E4%BF%A1%E4%BB%BB'
    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
             'Accept':'text/html;q=0.9,*/*;q=0.8',
             'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
             'Accept-Encoding':'gzip',
             'Connection':'close',
             'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
             }
    req_timeout = 5
    req = urllib2.Request(url,None,req_header)
    resp = urllib2.urlopen(req,None,req_timeout)
    html = resp.read()
    print(resp.info())

if __name__=='__main__':
    #crawl('/home/kehl/vocabs.txt')
    post()
        