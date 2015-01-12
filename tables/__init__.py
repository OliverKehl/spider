# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

DBSession = sessionmaker(autoflush=True,expire_on_commit=False)
DB_CONNECT_STRING = config.sqlalchemy_zidian_url

def init_session(CON=DB_CONNECT_STRING):
    global DBSession
    engine = create_engine(CON, echo=False)
    DBSession.configure(bind=engine)

init_session(DB_CONNECT_STRING)

if __name__=='__main__':
    print DB_CONNECT_STRING