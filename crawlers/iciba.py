# coding:utf-8
__author__='kehl'

import urllib2
import config
from tables.models import CidianInfo
from tables import DBSession
import time



host = 'http://hanyu.iciba.com'

def filter(str):
    str = str.replace('。','.')
    str = str.replace('～','~')
    str = str.replace('（','(')
    str = str.replace('）',')')
    return str

def extract_meaning(str):
    str = filter(str)
    l = str.split('<br />')
    if len(l)>1:
        l = l[1:]
    meaning = []
    liju = []
    for s in l:
        s = s[(s.rfind('</span>')+7):].strip()
        while True:
            wave = s.find('~')
            if wave>=0:
                end = s.find('.',wave)
                start = s.rfind('.',0,wave)
                liju.append(s[start+1:end+1].strip())
                s = s[:start+1]
            else:
                break
        meaning.append(s.strip())
    return meaning,liju

def extract_sentence(meta):
    index = str.find('[例句]')
    if index<0:
        return None
    left = meta.rfind('<li>',0,index)
    right = meta.find('</li>',index)
    meta = meta[left:right]
    meta = filter(meta)
    sens = meta.split('.')[0:-1]
    for s in sens:
        pass
        
#把gbk编码的字符串转换成utf8格式
#response = response.decode('gbk').encode('utf-8')

SIZE=1000

def crawl(filename):
    f = open(filename,'r')
    session = DBSession()
    reserved_words=[]
    not_exist_words = []
    try:
        for line in f.readlines():
            line = line.strip()
            url = 'http://hanyu.iciba.com/hy/'+line
            req = urllib2.urlopen(url)
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
            reserved_words.append(line)

            start = shiyi+8
            end = s.find('div',start)
            temp = s[start:end-1].strip()
            print temp

            cidianInfo = CidianInfo()
            #word
            cidianInfo.word = line

            #meaning and sentence
            meanings,sentences = extract_meaning(temp[0:temp.find('</li>')-5])
            cidianInfo.meaning = ''
            cidianInfo.sentence = ''
            for i in meanings:
                cidianInfo.meaning += i
            for i in sentences:
                cidianInfo.sentence += i.replace('~', ' '+line+' ')
            #print cidianInfo.meaning
            #print cidianInfo.sentence

            #sentence



            #synonym

            #antonym
            session.add(cidianInfo)
            count+=1
            if count==SIZE:
                session.commit()
                count = 0
                reserved_words=[]
        session.commit()
    except Exception,e:
        print e
        session.rollback()
        #TODO log reserved_words
    finally:
        session.close()

    time.sleep(3)

        

if __name__=='__main__':
    crawl('/home/kehl/vocabs.txt')
        
        
