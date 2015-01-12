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



    
    def __init__(self, zi = '', pinyin = '', bushou = '', 
    bihua = 0,jieshi = '' ):
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

def create_tables(dburl,echos=False):
    engine = create_engine(dburl,echo=echos)
    Base.metadata.create_all(engine)
    engine.dispose()

