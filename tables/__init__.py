# coding:utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

DBSession = sessionmaker(autoflush=True,expire_on_commit=False)
DB_CONNECT_STRING = config.sqlalchemy.zidian_url

def init_session(CON=DB_CONNECT_STRING):
    global DBSession
    engine = create_engine(CON, echo=False)
    DBSession.configure(bind=engine)

init_session(constants.database_str)
