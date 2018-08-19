import os

import sqlalchemy
from sqlalchemy import create_engine, Column, String, Date, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ['DATABASE_URL'])
Base = declarative_base()

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    page_id = Column(Integer)
    image_url = Column(String)
    page_url = Column(String)
    title = Column(String)
    created_at = Column(DateTime)

    def __repr__(self):
        return "<Post(date='%s', image_url='%s')>" % (self.date, self.image_url)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
