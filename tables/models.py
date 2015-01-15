# coding:utf-8
import sys,os
sys.path.append(os.path.dirname(os.getcwd()))

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,DateTime
import config

Base = declarative_base()

class ZidianInfo(Base):
    __tablename__='zidian'
    
    id = Column(Integer,primary_key=True)
    zi = Column(String(2), unique=True, index = True)
    pinyin = Column(String(10), index = True)
    bushou = Column(String(5), index = False)
    bihua = Column(Integer)
    jieshi = Column(String(200), index = True)
    zuci = Column(String(100)) #组词
    zaoju = Column(String(200))



    def __init__(self, zi = '', pinyin = '', bushou = '', bihua = 0,jieshi = '',zuci = '', zaoju = ''):
        self.zi = zi
        self.pinyin = pinyin
        self.bushou = bushou
        self.bihua = bihua
        self.jieshi = jieshi
        self.zuci = zuci
        self.zaoju = zaoju
    
    def __repr__(self):
        return "<Zidian Info('%s','%s','%s','%s','%s','%s',%s','%s','%s')>" %(self.zi,
                                                                             self.pinyin,
                                                                             self.bushou,
                                                                             str(self.bihua),
                                                                             self.jieshi,
                                                                             self.zuci,
                                                                             self.zaoju,
                                                                             )

class CidianInfo(Base):
    __tablename__='dictionary'
    
    id = Column(Integer,primary_key=True)
    word = Column(String(10), unique=True,index = True)
    tag = Column(String(5),index = True)
    pinyin = Column(String(30))
    meaning = Column(String(200))
    sentence = Column(String(100))
    synonym = Column(String(10))
    antonym = Column(String(10))
    
    def __init__(self,word='',tag='',pinyin='',meaning = '',sentence = '', synonym='', antonym = ''):
        self.word = word
        self.tag = tag
        self.pinyin = pinyin
        self.meaning = meaning
        self.sentence = sentence
        self.synonym = synonym
        self.antonym = antonym
        
    def __repr__(self):
        return "<Dictionary Info('%s','%s','%s','%s','%s','%s','%s')>" %(self.word,
                                                                            self.tag,
                                                                            self.pinyin,
                                                                             self.meaning,
                                                                             self.sentence,
                                                                             self.synonym,
                                                                             self.antonym,
                                                                             )

def create_tables(dburl,echos=False):
    engine = create_engine(dburl,echo=echos)
    Base.metadata.create_all(engine)
    engine.dispose()

if __name__=='__main__':
    create_tables(config.sqlalchemy_zidian_url)
