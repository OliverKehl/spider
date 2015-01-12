# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,DateTime

Base = declarative_base()

class ZidianInfo(Base):
    __tablename__='zidian'
    
    id = Column(Integer,primary_key=True)
    zi = Column(String(2),index = True)
    pinyin = Column(String(10), index = True)
    bushou = Column(String(5), index = False)
    bihua = Column(Integer)
    jieshi = Column(String(500), index = True)
    zuci = Column(String(100)) #组词
    zaoju = Column(String(300))



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
    word = Column(String(10),index = True)
    pinyin = Column(String(30))
    meaning = Column(String(200))
    sentence = Column(String(100))
    synonym = Column(String(10))
    antonym = Column(String(10))
    
    def __init__(self,word='',pinyin='',meaning = None,sentence = None, synonym=None, antonym = None):
        self.word = word
        self.pinyin = pinyin
        self.meaning = meaning
        self.sentence = sentence
        self.synonym = synonym
        self.antonym = antonym
        
    def __repr__(self):
        return "<Dictionary Info('%s','%s','%s','%s','%s','%s',%s','%s','%s')>" %(self.word,
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

