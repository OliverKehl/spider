# coding:utf-8
__author__='kehl'

import sys,os
sys.path.append(os.path.dirname(os.getcwd()))

import urllib2
from tables.models import CidianInfo
from tables import DBSession
import time



host = 'http://hanyu.iciba.com'

def filter(str):
    str = str.replace('。','.')
    str = str.replace('～','~')
    str = str.replace('（','(')
    str = str.replace('）',')')
    str = str.replace('、',',')
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
    sentences=[]
    index = meta.find('[例句]')
    if index<0:
        return sentences
    left = meta.rfind('<li>',0,index)
    right = meta.find('</li>',index)
    meta = meta[left:right]
    meta = filter(meta)
    sens = meta.split('.')[0:-1]
    for i in range(len(sens)):
        if i==0:
            s = sens[i][sens[i].rfind('</span>')+7:]
            sentences.append(s+'.')
        else:
            sentences.append(sens[i]+'.')
    return sentences

def extract_synonym(meta):
    synonyms=[]
    index = meta.find('[同义]')
    if index<0:
        return synonyms
    left = meta.rfind('<li>',0,index)
    right = meta.find('</li>',index)
    meta = meta[left:right]
    meta = filter(meta)
    syn = meta.split(',')
    for i in range(len(syn)):
        if i==0:
            synonyms.append(syn[i][syn[i].rfind('</span>')+7:])
        else:
            synonyms.append(syn[i])
    return synonyms     
    
def extract_antonym(meta):
    antonyms=[]
    index = meta.find('[反义]')
    if index<0:
        return antonyms
    left = meta.rfind('<li>',0,index)
    right = meta.find('</li>',index)
    meta = meta[left:right]
    meta = filter(meta)
    syn = meta.split(',')
    for i in range(len(syn)):
        if i==0:
            antonyms.append(syn[i][syn[i].rfind('</span>')+7:])
        else:
            antonyms.append(syn[i])
    return antonyms   

#<div class="js12"><font color="#008097">ài qíng</font>
def extract_pinyin(meta):
    left = meta.find('class=\"js12\">')
    right = meta.find('</font>',left)
    temp = meta[left:right]
    left = temp.rfind('>')
    return temp[left+1:]

#把gbk编码的字符串转换成utf8格式
#response = response.decode('gbk').encode('utf-8')

SIZE=1000

'''

</span>
       <span class="js211"></span><span class="js212"></span>(动)相信而敢于托付。        </li>
<li><span class="cy211">[同义]&nbsp;&nbsp;</span>信赖、相信</li>    
  </ul>
(动)相信而敢于托付

</span>
  <br />     <span class="js211">①</span><span class="js212"></span>（形）基本义：肯定的；正面的（跟‘消极’相对；多用于抽象事物）。起～作用。（作定语）    <br />     <span class="js211">②</span><span class="js212"></span>（形）进取的；热心的（跟‘消极’相对）。他对社会工作一向～。（作谓语）〈外〉日语。        </li>
      <li><span class="cy211">[构成]&nbsp;&nbsp;</span>并列式：积＋极</li>    <li><span class="cy211">[反义]&nbsp;&nbsp;</span>落后、消极</li>    
  </ul>
(形)基本义：肯定的；正面的(跟‘消极’相对；多用于抽象事物).(形)进取的；热心的(跟‘消极’相对).
起 积极 作用.他对社会工作一向 积极 .

'''

def crawl(filename):
    f = open(filename,'r')
    reserved_words=[]
    not_exist_words = []
    cidianInfos = []
    count = 0
    for line in f.readlines()[1:]:
        line = line.strip()
        print line
        if len(line.decode('utf8'))<2:
            continue
<<<<<<< HEAD
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
            reserved_words.append(line)
    
            start = shiyi+8
            end = s.find('div',start)
            temp = s[start:end-1].strip()
    
            cidianInfo = CidianInfo()
            #word
            cidianInfo.word = line
            
            #pinyin
            cidianInfo.pinyin = extract_pinyin(s)
            
            #meaning and sentence
            meanings,sentences = extract_meaning(temp[0:temp.find('</li>')-5])
            cidianInfo.meaning = ''.join(meanings)
            
            #sentence
            sentences2 = extract_sentence(s)
            sentences.extend(sentences2)
            cidianInfo.sentence = ''.join([t.replace('~',' '+line+' ') for t in sentences])
            #print cidianInfo.sentence
    
            #synonym
            synonyms = extract_synonym(s)
            cidianInfo.synonym = '.'.join(synonyms)
            #print cidianInfo.synonym
            
            #antonym
            antonyms = extract_antonym(s)
            cidianInfo.antonym = '.'.join(antonyms)
            
            count+=1
            cidianInfos.append(cidianInfo)
            if count==SIZE:
                addToDB(cidianInfos,reserved_words)
                count = 0
                reserved_words=[]
                cidianInfos = []
            time.sleep(1)
        except Exception , e:
            print e
    addToDB(cidianInfos,reserved_words)

def addToDB(cidianInfos,words):
    session = DBSession()
    try:
        for info in cidianInfos:
            session.add(info)
            session.commit()
    except Exception,e:
        #TODO log reserved_words
        print e
        session.rollback()
    finally:
        session.close()
        
    

if __name__=='__main__':
    import os,sys
    crawl(os.path.dirname(os.getcwd())+'/data/vocab.txt')
    
        
        
